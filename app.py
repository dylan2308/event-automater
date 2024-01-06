import datetime
import os.path

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

from google_auth_oauthlib.flow import InstalledAppFlow

# Scope of access, i.e. what you want user to access
SCOPES = ["https://www.googleapis.com/auth/calendar"]

def main():
  creds = None # None is python equivalent of null; class = "Credentials"

  # "token.json" stores user's Access Tokens(will expire) & Refresh Tokens(used to acquire new Access Token)
  # Search for "token.json" file, if present, returns the constructed credentials;
  # usage: ...Credentials...user_file(filename, scope="...")
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)

  # If there are no (valid) credentials available, let the user log in.
  # Credentials.valid return boolean True if valid vice versa
  # None is evaluated to False; and if not None it evaluates to True
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
      creds = flow.run_local_server(port=0)

    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())


  event = {
    "summary": "testEvent",

    "start": {
      "dateTime": "2024-01-10T10:00:00+08:00",
      "timeZone": "Asia/Singapore"
    },

    "end": {
      "dateTime": "2024-01-11T10:00:00+08:00",
      "timeZone": "Asia/Singapore"
    }
  }

  try:
    # Create service object; usage: build(serviceName, version, ..., credentials="...")
    service = build("calendar", "v3", credentials = creds)
    event = service.events().insert(calendarId = "primary", body = event).execute()

  except HttpError as error:
    print(f"Http Error occurred: {error}")

if __name__ == "__main__":
  main()
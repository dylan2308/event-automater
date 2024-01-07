import ask
import helper
import datetime as dt
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

  title = input("Event Title: ")

  startDate, startTime, endDate, endTime = ['a', 'a', 'a', 'a']
  # Start Date
  while(helper.is_valid_date(startDate) == False):
    startDate = input('Enter start date in the format DD/MM/YYYY: ')  
            
  # Check Start Time
  while(helper.is_valid_time(startTime) == False):
    time_input = input('Enter start time in the format HHMM: ')
    startTime = time_input[:2] + ':' + time_input[2:] + ':00'

  # Check end Date
  while(helper.is_valid_date(endDate) == False):
    endDate = input('Enter end date in the format YYYY-MM-DD: ')

  #Check end time
  while(helper.is_valid_time(endTime) == False):
    time_input = input('Enter end time in the format HHMM: ')
    endTime = time_input[:2] + ':' + time_input[2:] + ':00'

  event = {
    "summary": f"{title}",

    "start": {
      "dateTime": f"{startDate}T{startTime}",
      "timeZone": "Asia/Singapore"
    },

    "end": {
      "dateTime": f"{endDate}T{endTime}",
      "timeZone": "Asia/Singapore"
    },

    "reminders": {
      "useDefault": "False",
      "overrides": [
        {
          "method": "popup",
          "minutes": "360"
        },
        {
          "method" : "popup",
          "minutes": "180"
        }
      ]
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
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

  title = input("Event Title: ")
          
  startYear, startMth, startDay, startHr, startMin, startS = [0, 0, 0, 0, 0, 0]
  endYear, endMth, endDay, endHr, endMin, endS = [0, 0, 0, 0, 0, 0]

  # Check valid year
  while startYear < 2024 or startYear > 2100:
      while True:
          try:
              startYear = int(input("Enter a valid start year: "))
              break
          except:
              continue
  # Check valid month i.e. between 1-12
  while startMth not in range(1, 13):
      while True:
          try:
              startMth = int(input("Enter a valid start month: "))
              break
          except:
              continue
  # Check months with 31 days
  if startMth in [1, 3, 5, 7, 8, 10, 12]:
      while startDay not in range(1, 32):
          while True:
              try:
                  startDay = int(input("Enter a valid start day: "))
                  break
              except:
                  continue
  # Check months with 30 days
  elif startMth in [4, 6, 9, 11]:
      while startDay not in range(1, 31):
          while True:
              try:
                  startDay = int(input("Enter a valid start day: "))
                  break
              except:
                  continue
  # Check February
  elif startMth == 2:
      # Leap years are divisible by 4
      if startYear % 4 == 0:
          while startDay not in range(1, 30):
              while True:
                  try:
                      startDay = int(input("Enter a valid start day: "))
                      break
                  except:
                      continue
      else:
          while startDay not in range(1, 29):
              while True:
                  try:
                      startDay = int(input("Enter a valid start day: "))
                      break
                  except:
                      continue
  
  startDate = str(startYear) + "-" + str(startMth) + "-" + str(startDay)

  event = {
    "summary": f"{title}",

    "start": {
      "dateTime": f"{startDate}T10:00:00",
      "timeZone": "Asia/Singapore"
    },

    "end": {
      "dateTime": "2024-01-11T10:00:00",
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
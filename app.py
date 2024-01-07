import ask
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

  startYear, startMth, startDay, endYear, endMth, endDay = [0, 0, 0, 0, 0, 0]
  startHr, startMin, startS, endHr, endMin, endS = [-1, -1, -1, -1, -1, -1]

  # Check Start Date
  # Check valid year
  while startYear < 2024 or startYear > 2100:
    startYear = ask.askStartYr()
  # Check valid month i.e. between 1-12
  while startMth not in range(1, 13):
    startMth = ask.askStartMth()
  # Check months with 31 days
  if startMth in [1, 3, 5, 7, 8, 10, 12]:
    while startDay not in range(1, 32):
      startDay = ask.askStartDay()
  # Check months with 30 days
  elif startMth in [4, 6, 9, 11]:
    while startDay not in range(1, 31):
      startDay = ask.askStartDay()
  # Check February
  elif startMth == 2:
    # Leap years are divisible by 4
    if startYear % 4 == 0:
      while startDay not in range(1, 30):
        startDay = ask.askStartDay()
    else:
      while startDay not in range(1, 29):
        startDay = ask.askStartDay()

  # Check Start Time
  # Check valid hour
  while startHr not in range(0, 24):
    startHr = ask.askStartHr()
  # Check valid min
  while startMin not in range(0, 60):
    startMin = ask.askStartMin()
  # Check valid sec
  while startS not in range(0, 60):
    startS = ask.askStartS()

  # Check End Date
  # Check valid year
  while endYear < 2024 or endYear > 2100:
    endYear = ask.askEndYr()
  # Check valid month i.e. between 1-12
  while endMth not in range(1, 13):
    endMth = ask.askEndMth()
  # Check months with 31 days
  if endMth in [1, 3, 5, 7, 8, 10, 12]:
    while endDay not in range(1, 32):
      endDay = ask.askEndDay()
  # Check months with 30 days
  elif endMth in [4, 6, 9, 11]:
    while endDay not in range(1, 31):
      endDay = ask.askEndDay()
  # Check February
  elif endMth == 2:
    # Leap years are divisible by 4
    if endYear % 4 == 0:
      while endDay not in range(1, 30):
        endDay = ask.askEndDay()
    else:
      while endDay not in range(1, 29):
        endDay = ask.askEndDay()

  # Check End Time
  # Check valid hour
  while endHr not in range(0, 24):
    endHr = ask.askEndHr()
  # Check valid min
  while endMin not in range(0, 60):
    endMin = ask.askEndMin()
  # Check valid sec
  while endS not in range(0, 60):
    endS = ask.askEndS()
              
  startDate = str(startYear) + "-" + str(startMth) + "-" + str(startDay)
  startTime = str(startHr) + ":" + str(startMin) + ":" + str(startS)

  endDate = str(endYear) + "-" + str(endMth) + "-" + str(endDay)
  endTime = str(endHr) + ":" + str(endMin) + ":" + str(endS)

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
from helper import is_valid_date, is_valid_time, convert_date, convert_time
import os.path

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

from google_auth_oauthlib.flow import InstalledAppFlow

# modules for telegram bot
from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN: Final = '6630171420:AAH9TrksYVzYeOw60caThg7dOwTzAdTN1zY'
BOT_USERNAME: Final = 'google_calendardyl_bot'


# telegram bot is to take in user input for the variables below, title, startDate, startTime, endDate and endTime, the code can be written within main()
# example of valid user input eventName startDate startTime endDate endTime, e.g. Dental 27/01/2024 1500 27/01/2024 1600

# commands
async def start_command(update: Update, context: ContextTypes):
  await update.message.reply_text('Hello, I can help you add events to your Google Calendar!')
  await update.message.reply_text('Input your event in the following format: EventName StartDate EndDate StartTime EndTime, example: Dental 27/01/2024 27/01/2024 1500 1700')


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
  await update.message.reply_text('I am a bot that adds your events to your google calendar, please type something so I can respond!')

# Handle responses
async def handle_response(update: Update, context: ContextTypes):
    text = update.message.text
    response = text.split()
    if len(response) != 5:
        await update.message.reply_text('Invalid response, please check that you have inputted a valid date and time!')
        return
    
    title, startDate, endDate, startTime, endTime = response[0], response[1], response[2], response[3], response[4]
    
    if is_valid_date(startDate) == False or is_valid_date(endDate) == False or is_valid_time(convert_time(startTime)) == False or is_valid_time(convert_time(endTime)) == False:
        return 'Invalid response, please check that you have inputted a valid date and time!'
    elif is_valid_date(startDate) and is_valid_date(endDate) and is_valid_time(convert_time(startTime)) and is_valid_time(convert_time(endTime)):
        print('Valid Response')
        startDate, endDate, startTime, endTime = convert_date(startDate), convert_date(endDate), convert_time(startTime), convert_time(endTime)
        main(title, startDate, endDate, startTime, endTime, update)
        await update.message.reply_text('Event created successfully!')
    else:
        await update.message.reply_text('I do not understand. Please try again with a valid input! Or try /help')

# Scope of access, i.e. what you want user to access
SCOPES = ["https://www.googleapis.com/auth/calendar"]

def main(title, startDate, endDate, startTime, endTime, update):
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

  # print authentication details for debugging  
  print('Authentication Details: ', creds.to_json())

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

  # print event details for debugging
  print('Event Details: ', event)

  try:
    # Create service object; usage: build(serviceName, version, ..., credentials="...")
    service = build("calendar", "v3", credentials = creds)
    event = service.events().insert(calendarId = "primary", body = event).execute()

  except HttpError as error:
    print(f"Http Error occurred: {error}")

if __name__ == "__main__":
    print('Starting bot...')
    app = Application.builder().token(TOKEN).build()

    # commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))

    # messages
    app.add_handler(MessageHandler(filters.TEXT, handle_response))

    # polls the bot, checks for new messages every 3 seconds
    print('Polling...')
    app.run_polling(poll_interval=3)
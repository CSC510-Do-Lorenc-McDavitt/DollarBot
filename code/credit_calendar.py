import helper
from telebot import types
from dotenv import load_dotenv
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from datetime import datetime, timedelta

import os
# === Documentation of credit_calendar.py ===

account_names = {}


def run(message, bot):
    """
    run(message, bot): This is the main function used to implement the calendar
    due date credit feature
    """
    chat_id = message.chat.id
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.row_width = 2
    credit_list = helper.read_credit_json()
    if (not credit_list
        or str(chat_id) not in credit_list
            or len(credit_list[str(chat_id)].keys()) == 0):
        bot.send_message(chat_id, "You do not have any credit accounts!")
        return
    for c in credit_list[str(chat_id)].keys():
        markup.add(c)
    msg = bot.send_message(chat_id,
                           "Which account do you want to add the due dates in your calendar for?",
                           reply_markup=markup)
    bot.register_next_step_handler(msg, handle_account_name, bot)


def handle_account_name(message, bot):
    """
    Handles the input of the group name for setting up a due date for a credit account
    """
    chat_id = message.chat.id
    credit_list = helper.read_credit_json()
    if (not credit_list or len(credit_list) == 0 or str(chat_id) not in credit_list):
        helper.write_credit_json({str(chat_id): {}})
    credit_list = helper.read_credit_json()
    account_names[chat_id] = str(message.text)
    account_name = account_names[chat_id]
    if (account_name not in credit_list[str(chat_id)].keys()):
        bot.send_message(chat_id, "That account name doesn't exist!")
        return
    credit_list[str(chat_id)][account_name]["expenses"] = []
    helper.write_credit_json(credit_list)
    oauth2_url = f'https://accounts.google.com/o/oauth2/v2/auth?response_type=code&client_id={os.getenv("CLIENT_ID")}&redirect_uri=http://localhost:5000/oauth2callback&scope=https://www.googleapis.com/auth/calendar&state={chat_id}'
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.row_width = 2
    markup.add("Done")
    markup.add("Cancel")
    bot.send_message(chat_id, f"{oauth2_url}\nPlease enter \"done\" when you are finished setting it up.",
                     reply_markup=markup)
    bot.register_next_step_handler(message, handle_oauth, bot)


def handle_oauth(message, bot):
    """
    Handles the using of the oauth token of the group name 
    for setting up a due date for a credit account
    """
    try:
        chat_id = message.chat.id
        credit_list = helper.read_credit_json()
        if str(message.text).lower() != "done":
            bot.send_message(chat_id, "Transaction canceled")
            return
        if (not credit_list
            or str(chat_id) not in credit_list
                or len(credit_list[str(chat_id)].keys()) == 0):
            bot.send_message(chat_id, "You do not have any credit accounts!")
            return

        account_name = account_names[chat_id]
        if account_name not in credit_list[str(chat_id)].keys():
            bot.send_message(chat_id, "That account name doesn't exist!")
            return

        # Get the current date
        today = datetime.utcnow().date()
        today = today.replace(
            day=credit_list[str(chat_id)][account_name]["due date"])
        event = {
            "summary": "Pay Credit Account For: " + account_name,
            "description": "Pay off your credit card fees before it's too late!\
                The account is for " + account_name,
            "start": {
                "date": str(today.isoformat()),
            },
            "end": {
                "date": str((today + timedelta(days=1)).isoformat()),
            },
            "recurrence": [
                "RRULE:FREQ=MONTHLY;BYMONTHDAY=" +
                str(credit_list[str(chat_id)][account_name]["due date"])
            ],
            "reminders": {
                "useDefault": False,
                "overrides": [
                    {"method": "email", "minutes": 24 * 60},  # 24 hours before
                    {"method": "popup", "minutes": 30}
                ]
            }
        }
        oauth_record = helper.read_oauth_json()
        if str(chat_id) not in oauth_record:
            bot.send_message(
                chat_id, "Your oauth2 token was not generated properly!")
            return
        token = oauth_record[str(chat_id)]["access_token"]
        creds = Credentials(token)
        service = build("calendar", "v3", credentials=creds)

        # Insert the event into the primary calendar
        created_event = service.events().insert(
            calendarId="primary", body=event).execute()
        credit_list[str(chat_id)][account_name]["calendar"] = True
        helper.write_credit_json(credit_list)
        bot.send_message(
            chat_id, "Successfully added the calendar event for " + account_name)
    except Exception as e:
        print(str(e))
        bot.send_message(
            chat_id, "Sorry, something went wrong. Try again later!")

import helper
import logging
from telebot import types
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP
from datetime import datetime

# === Documentation of credit_view.py ===

def run(message, bot):
    """
    run(message, bot): This is the main function used to implement the add feature.
    It prompts the user to decide whether to add the expense to a group or a category.
    """
    chat_id = message.chat.id

    bot.send_message(chat_id, display_credit(chat_id))

def display_credit(chat_id):
    credit_list = helper.read_credit_json()
    if(not credit_list or len(credit_list) == 0 or str(chat_id) not in credit_list):
        return "You currently have no credit records."
    output = ["Showing Accounts and Credit Expenses:",
              "------------------------------------------------------"]
    for account in credit_list[str(chat_id)]:
        output.append(account)
        output.append("  Expenses")
        for x in credit_list[str(chat_id)][account]["expenses"]:
            output.append("    " + x)
        output.append("  Monthly Due Date: " + str(credit_list[str(chat_id)][account]["due date"]))
        output.append("  Currently Owing: " + str(credit_list[str(chat_id)][account]["owe"]))
        output.append(("  Calendar is currently set up for this event" 
                       if credit_list[str(chat_id)][account]["calendar"] 
                       else "  No Calendar currently set up"))
        output.append("------------------------------------------------------")
    return "\n".join(output)
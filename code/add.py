"""
File: add.py
Author: Vyshnavi Adusumelli, Tejaswini Panati, Harshavardhan Bandaru
Date: October 01, 2023
Description: File contains Telegram bot message handlers and their associated functions.

Copyright (c) 2023

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS," WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import random
import string
import helper
import logging
from telebot import types
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from dotenv import load_dotenv
import os
load_dotenv()
option = {}

""" Length the Hash should be for group expenses """
HASH_LENGTH = 16

""" Collection of all ASCII letters and numbers """
LETTERS_AND_DIGITS = string.ascii_letters + string.digits
# === Documentation of add.py ===


class Group_Name:
    """ 
    Class to store updates to the individual or group
    that is being worked with
    """

    def __init__(self):
        """ initialize the class """
        self.group_name = False

    def update_group(self, new_group):
        """ 
        Update the group we are working with
        (False) = individual
        """
        self.group_name = new_group


""" Class for the group """
user_group = Group_Name()


def generate_random_group_expense_hash():
    """ Create a Random Key for Group Expenses """
    return ''.join([random.choice(LETTERS_AND_DIGITS) for _ in range(HASH_LENGTH)])


def run(message, bot):
    """
    run(message, bot): This is the main function used to implement the add feature.
    It prompts the user to decide whether to add the expense to a group or a category.
    """
    chat_id = message.chat.id
    markup = types.ReplyKeyboardMarkup(
        one_time_keyboard=True, resize_keyboard=True)
    markup.row_width = 2
    markup.add(types.KeyboardButton("Individual"),
               types.KeyboardButton("Group"))

    # Reset the option for the current user when starting a new flow
    option[chat_id] = {}  # Reset the option for the current user

    msg = bot.send_message(
        chat_id, "Do you want to add this expense to an individual or a group?", reply_markup=markup)
    bot.register_next_step_handler(msg, handle_group_check, bot)


def handle_group_check(message, bot):
    """
    Handles whether the user wants to add the expense to a group or not based on button selection.
    """
    chat_id = message.chat.id
    choice = message.text.lower()

    if choice == "group":
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.row_width = 2
        groups = helper.load_group_data()
        if not groups:
            bot.message_send(
                "There are currently no groups. Add them with /group")
            return
        for key in groups.keys():
            markup.add(key)
        msg = bot.send_message(
            chat_id, "Enter the group name:", reply_markup=markup)
        bot.register_next_step_handler(msg, handle_group_name, bot)
    elif choice == "individual":
        user_group.update_group(False)
        msg = bot.send_message(chat_id, "Select date")
        calendar, step = DetailedTelegramCalendar().build()
        bot.send_message(
            chat_id, f"Select {LSTEP[step]}", reply_markup=calendar)

        @bot.callback_query_handler(func=DetailedTelegramCalendar.func())
        def cal(c):
            chat_id = c.message.chat.id
            result, key, step = DetailedTelegramCalendar().process(c.data)

            if not result and key:
                bot.edit_message_text(
                    f"Select {LSTEP[step]}",
                    chat_id,
                    c.message.message_id,
                    reply_markup=key,
                )
            elif result:
                data = datetime.today().date()
                if result > data:
                    bot.send_message(
                        chat_id, "Cannot select future dates. Please try /add command again with correct dates.")
                else:
                    # group_name=None means individual flow
                    category_selection(message, bot, result)
    else:
        bot.send_message(
            chat_id, "Invalid choice. Please choose from the buttons.")


def handle_group_name(message, bot):
    """
    Handles adding expenses to the specified group.
    Ensures that the group exists before proceeding to add the expense.
    """
    chat_id = message.chat.id
    group_name = message.text
    user_group.update_group(message.text)

    groups = helper.load_group_data()

    if groups and group_name in groups:
        # Store the group name in the option dictionary for the current user
        # Track group name in option
        option[chat_id]['group_name'] = group_name

        # Proceed to ask for date for group expense
        msg = bot.send_message(chat_id, "Select date")
        calendar, step = DetailedTelegramCalendar().build()
        bot.send_message(
            chat_id, f"Select {LSTEP[step]}", reply_markup=calendar)

        @bot.callback_query_handler(func=DetailedTelegramCalendar.func())
        def cal(c):
            chat_id = c.message.chat.id
            result, key, step = DetailedTelegramCalendar().process(c.data)

            if not result and key:
                bot.edit_message_text(
                    f"Select {LSTEP[step]}",
                    chat_id,
                    c.message.message_id,
                    reply_markup=key,
                )
            elif result:
                data = datetime.today().date()
                if result > data:
                    bot.send_message(
                        chat_id, "Cannot select future dates. Please try /add command again with correct dates.")
                else:
                    # Pass group_name for group flow
                    category_selection(message, bot, result, group_name)
    else:
        bot.send_message(
            chat_id, f"Group '{group_name}' does not exist. Please create a new group with /group.")


def category_selection(msg, bot, date, group_name=None):
    """
    Handles the selection of expense categories for both individuals and groups.
    If group_name is None, it's an individual expense.
    """
    try:
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.row_width = 2
        categories = helper.getSpendCategories()
        if not categories:
            bot.reply_to(
                msg, "You don't have any categories. Please add a category!!")
        else:
            for c in categories:
                markup.add(c)
            msg = bot.reply_to(msg, "Select Category", reply_markup=markup)
            bot.register_next_step_handler(
                msg, post_category_selection, bot, date, group_name)
    except Exception as e:
        print(e)


def post_category_selection(message, bot, date, group_name=None):
    """
    Processes the selected category and asks for the expense amount.
    Handles both individual and group flows based on the presence of group_name.
    """
    try:
        chat_id = message.chat.id
        selected_category = message.text
        if selected_category not in helper.getSpendCategories():
            bot.send_message(
                chat_id, "Invalid", reply_markup=types.ReplyKeyboardRemove()
            )
            raise Exception(
                'Sorry, I don\'t recognise this category "{}"!'.format(
                    selected_category)
            )

        # Store the category in the option dictionary
        option[chat_id]['category'] = selected_category

        msg = bot.send_message(
            chat_id, "How much did you spend on {}? \n(Numeric values only)".format(
                str(option[chat_id]['category'])),
        )
        bot.register_next_step_handler(
            msg, post_amount_input, bot, selected_category, date)
    except Exception as e:
        logging.exception(str(e))
        bot.reply_to(message, "Oh no! " + str(e))


def post_amount_input(message, bot, selected_category, date, group_name=None):
    """
    Handles the input of the expense amount and stores it.
    Works for both individual and group expenses.
    """
    name_for_group = group_name if group_name else user_group.group_name
    print(name_for_group)
    try:
        chat_id = message.chat.id
        amount_entered = message.text

        # Ensure the amount is converted to a float (will raise ValueError if invalid)
        amount_value = float(helper.validate_entered_amount(
            amount_entered))  # validate

        if amount_value == 0:  # cannot be $0 spending
            raise Exception("Spent amount has to be a non-zero number.")

        date_of_entry = date.strftime(helper.getDateFormat())
        date_str, category_str, amount_str = (
            str(date_of_entry),
            str(selected_category),
            str(amount_value),
        )

        if name_for_group:  # Group flow
            groups = helper.load_group_data()
            expense_hash = generate_random_group_expense_hash()
            # Convert amount_value to a float if it isn't already
            expense_record = {
                "date": date_str,
                "category": category_str,
                "amount": amount_value,
                "hash": expense_hash
            }
            groups[name_for_group]['expenses'].append(expense_record)

            # Make sure 'total_spent' is a float to allow addition
            groups[name_for_group]['total_spent'] += amount_value

            # Calculate the per-member share
            group_size = groups[name_for_group]['size']
            per_member_share = groups[name_for_group]['total_spent'] / group_size
            split_amount = amount_value / group_size
            group_emails = groups[name_for_group]["emails"]
            # Persist the updated group data
            helper.save_group_data(groups)

            bot.send_message(
                chat_id, f"Expense of ${amount_value} for '{category_str}' added to group '{name_for_group}' on {date_str}.")
            bot.send_message(
                chat_id, f"Each member now owes: ${per_member_share:.2f}")
            if group_emails and len(group_emails) > 0:
                markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
                markup.row_width = 2
                markup.add("Yes")
                markup.add("No")
                msg = bot.send_message(chat_id,
                                       "Would you like to send an email to each member for this expense?",
                                       reply_markup=markup)
                bot.register_next_step_handler(
                    msg, handle_group_email, bot, group_emails, per_member_share, name_for_group, split_amount)
            helper.write_json(
                add_user_record(
                    chat_id, "{},{},{},{},{}".format(
                        date_str, category_str, str(float(amount_str) / group_size), name_for_group, expense_hash), expense_hash
                )
            )

        else:  # Individual flow
            helper.write_json(
                add_user_record(
                    chat_id, "{},{},{}".format(
                        date_str, category_str, amount_str)
                )
            )
            bot.send_message(
                chat_id,
                "The following expenditure has been recorded: You have spent ${} for {} on {}".format(
                    amount_str, category_str, date_str
                ),
            )
            helper.display_remaining_budget(message, bot)
            record = "{},{},{}".format(date_str, category_str, amount_str)
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.row_width = 2
            markup.add("Yes")
            markup.add("No")
            msg = bot.send_message(
                chat_id, "Do you want to add this expense to your credit account for tracking?",
                reply_markup=markup)
            bot.register_next_step_handler(msg, credit_option, bot, record)
    except ValueError:
        bot.send_message(
            chat_id, "Please enter a valid number for the expense.")
    except Exception as e:
        logging.exception(str(e))
        bot.send_message(chat_id, "Oh no. " + str(e))


def handle_group_email(message, bot, group_emails, per_member_share, group_name, split_amount):
    """
    Handles the event of sending a group email regarding the expense split.
    """
    chat_id = message.chat.id
    try:
        if str(message.text).lower() == "yes":
            mail_content = f'''Hello,
                        This email is to inform you of a split expense cost. Be sure
                        to pay it back soon!
                        Current expense cost of group {group_name}:
                        The recent expense generated(your split): ${"{:.2f}".format(split_amount)}
                        Your total expenses for the group: ${"{:.2f}".format(per_member_share)}
                        Thank you!
                        '''
            # The mail addresses and password
            sender_address = os.getenv("EMAIL")
            sender_pass = os.getenv("EMAIL_PASS")

            # Setup the MIME
            message = MIMEMultipart()
            message['From'] = sender_address
            message['Subject'] = 'Group Expense Added'
            # The subject line
            # The body and the attachments for the mail
            message.attach(MIMEText(mail_content, 'plain'))
            # Create SMTP session for sending the mail
            # use gmail with port
            session = smtplib.SMTP('smtp.gmail.com', 587)
            session.starttls()  # enable security
            # login with mail_id and password
            session.login(sender_address, sender_pass)
            text = message.as_string()
            for email in group_emails:
                receiver_address = email
                message['To'] = receiver_address
                session.sendmail(sender_address, receiver_address, text)
            session.quit()
            bot.send_message(chat_id, "Mail Sent")
        else:
            bot.send_message(chat_id, "Email was not generated.")
    except Exception:
        bot.send_message(chat_id, "Somethign went wrong")


def credit_option(message, bot, record):
    """
    This function handles if the user wants to put the
    expense under their credit account to track it
    """
    chat_id = message.chat.id
    credit_list = helper.read_credit_json()
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.row_width = 2
    if str(message.text).lower() == "yes":

        if (not credit_list
            or str(chat_id) not in credit_list
                or len(credit_list[str(chat_id)].keys()) == 0):
            msg = bot.send_message(
                chat_id, "You currently don't have any credit accounts.",
            )
            return
        for c in credit_list[str(chat_id)].keys():
            markup.add(c)
        else:
            msg = bot.send_message(
                chat_id, "Which account do you want to add it to?", reply_markup=markup
            )
            bot.register_next_step_handler(msg, credit_name_input, bot, record)
    elif str(message.text).lower() == "no":
        msg = bot.send_message(
            chat_id, "Alright, thank you!"
        )
        return
    else:
        markup.add("Yes")
        markup.add("No")
        msg = bot.send_message(
            chat_id, "Do you want to add this expense to your credit account for tracking?",
            reply_markup=markup)
        bot.register_next_step_handler(msg, credit_option, bot, record)


def credit_name_input(message, bot, record):
    """
    This function handles putting the expense
    under the credit account depending on the name.
    """
    chat_id = message.chat.id
    try:
        credit_list = helper.read_credit_json()
        account_name = str(message.text)
        if (account_name not in credit_list[str(chat_id)].keys()):
            bot.send_message(chat_id, "That account name doesn't exist!")
            return
        credit_list[str(chat_id)][account_name]["expenses"].append(record)
        bot.send_message(
            chat_id, "Expenditure added to credit account: " + account_name)
        owe_pre = credit_list[str(chat_id)][account_name]["owe"]
        amount = float(record.split(",")[-1])
        credit_list[str(chat_id)][account_name]["owe"] += amount
        owe_now = credit_list[str(chat_id)][account_name]["owe"]
        helper.write_credit_json(credit_list)
        bot.send_message(
            chat_id,
            "What you owe for the account now $" +
            "{:.2f}".format(owe_pre) + " --> $" + "{:.2f}".format(owe_now))
    except ValueError:
        bot.send_message(
            chat_id, "Please enter a valid number for the expense.")
    except Exception as e:
        bot.send_message(chat_id, "Oh no. " + str(e))


def add_user_record(chat_id, record_to_be_added, grouphash=None):
    """
    Stores the expense record for the user.
    """
    user_list = helper.read_json()
    if user_list is None:
        user_list = {}

    if str(chat_id) not in user_list:
        user_list[str(chat_id)] = helper.createNewUserRecord()

    if not grouphash:
        user_list[str(chat_id)]["data"].append(record_to_be_added)
    else:
        if not user_list[str(chat_id)].get("groupdata", None):
            user_list[str(chat_id)]["groupdata"] = []
        user_list[str(chat_id)]["groupdata"].append(record_to_be_added)
    return user_list

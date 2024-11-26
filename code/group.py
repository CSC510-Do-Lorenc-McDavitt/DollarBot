"""
File: group.py
Author: Yumo Shen
Date: October, 2024
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

import helper
from telebot import types
import re

groups = helper.load_group_data()  # Load group data from persistent storage
group_emails = {}


def run(message, bot):
    """
    Main function to handle group-related actions: view, create, or delete a group.
    """
    chat_id = message.chat.id
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.row_width = 2
    markup.add("Create Group", "View All Groups", "Delete Group")
    msg = bot.send_message(chat_id, "Choose an option:", reply_markup=markup)
    group_emails[chat_id] = []
    bot.register_next_step_handler(msg, handle_group_action, bot)


def handle_group_action(message, bot):
    """
    Handles the selection of the group action: creating, viewing, or deleting a group.
    """
    chat_id = message.chat.id
    selected_action = message.text

    if selected_action == "Create Group":
        msg = bot.send_message(chat_id, "Enter the name of the group:")
        bot.register_next_step_handler(msg, handle_group_name, bot)
    elif selected_action == "View All Groups":
        view_all_groups(chat_id, bot)
    elif selected_action == "Delete Group":
        msg = bot.send_message(
            chat_id, "Enter the name of the group you want to delete:")
        bot.register_next_step_handler(msg, handle_delete_group, bot)
    else:
        bot.send_message(chat_id, "Invalid option. Please try again.")
        run(message, bot)


def handle_group_name(message, bot):
    """
    Handles the input of the group name for creating a new group.
    """
    chat_id = message.chat.id
    group_name = message.text

    if group_name in groups:
        bot.send_message(
            chat_id, f"Group '{group_name}' already exists. You can add expenses to it via /add.")
    else:
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.row_width = 2
        markup.add("Yes")
        markup.add("No")
        msg = bot.send_message(
            chat_id, "Do you want to add group member emails to this group?",
            reply_markup=markup)
        bot.register_next_step_handler(
            msg, handle_group_email_question, bot, group_name)


def handle_group_email_question(message, bot, group_name):
    """
    Handles asking if the user wants to add emails and
    does the loop to add all of the emails
    """
    chat_id = message.chat.id
    if str(message.text).lower() == "yes":
        msg = bot.send_message(
            chat_id, "Please type each email you want to add and submit one at a time. Type done when you are finished.")
        bot.register_next_step_handler(
            msg, handle_group_email, bot, group_name)
    else:
        bot.send_message(chat_id, "Skipping the group email process...")
        msg = bot.send_message(
            chat_id, f"Group '{group_name}' does not exist. Enter the group size:")
        bot.register_next_step_handler(msg, create_group, bot, group_name)


def handle_group_email(message, bot, group_name):
    """
    Handle the looping gropu emails
    """
    chat_id = message.chat.id
    if str(message.text).lower() == "done":
        bot.send_message(chat_id, "Finalizing the group creation process")
        msg = bot.send_message(
            chat_id, f"Group '{group_name}' does not exist. Enter the group size:")
        bot.register_next_step_handler(msg, create_group, bot, group_name)
        return
    if is_valid_email(str(message.text)):
        group_emails[chat_id].append(str(message.text))
        msg = bot.send_message(
            chat_id, "Next email please, or type done if you are finished")
        bot.register_next_step_handler(
            msg, handle_group_email, bot, group_name)
    else:
        msg = bot.send_message(
            chat_id, "That is not a valid email, please try again!")
        bot.register_next_step_handler(
            msg, handle_group_email, bot, group_name)


def create_group(message, bot, group_name):
    """
    Creates a new group with the specified name and size, and saves the group data.
    """
    try:
        chat_id = message.chat.id
        group_size = int(message.text)  # Validate input

        # Create a new group entry with an empty 'expenses' list
        groups[group_name] = {"size": group_size,
                              "total_spent": 0, "expenses": [],
                              "emails": group_emails[chat_id]}

        # Persist the new group data
        helper.save_group_data(groups)

        # Notify the user that the group has been created
        bot.send_message(
            chat_id, f"Group '{group_name}' created with {group_size} members.")
        msg = bot.send_message(
            chat_id, "You can add expenses to this group using the /add command.")
    except ValueError:
        msg = bot.send_message(
            chat_id, "Please enter a valid number for group size.")
        bot.register_next_step_handler(msg, create_group, bot, group_name)
        return


def view_all_groups(chat_id, bot):
    """
    Displays all the existing groups.
    """
    if groups:
        group_list = "\n".join([str(key) + "\n  " +
                                ("\n  ".join(groups[key]["emails"])
                                 if groups[key]["emails"] and
                                 len(groups[key]["emails"]) > 0
                                 else
                                 "No emails"
                                 )
                                for key in groups.keys()])
        bot.send_message(chat_id, f"Here are all the groups:\n{group_list}")
    else:
        bot.send_message(
            chat_id, "No groups available. Please create a group using the /group command.")


def handle_delete_group(message, bot):
    """
    Handles deleting the specified group and its associated expenses.
    """
    chat_id = message.chat.id
    group_name = message.text

    if group_name in groups:
        # Delete the group and its associated expenses
        del groups[group_name]

        # Persist the updated group data
        helper.save_group_data(groups)

        bot.send_message(
            chat_id, f"Group '{group_name}' and all associated expenses have been deleted.")
    else:
        bot.send_message(chat_id, f"Group '{group_name}' does not exist.")


def is_valid_email(email):
    """
    Validate email using regex
    """
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(pattern, email) is not None

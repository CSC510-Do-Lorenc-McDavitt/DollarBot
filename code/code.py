"""
File: code.py
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


#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import logging
import telebot
import time
import helper
import edit
import history
import pdf
import display
import estimate
import delete
import add
import budget
import analytics
import predict
import updateCategory
import weekly
import monthly
import sendEmail
import add_recurring
import group
import chat
import portfolio
import credit_view
import credit_setup
import credit_pay
import credit_clear
import credit_delete
import credit_calendar
import threading
import requests
from datetime import datetime, timedelta
from jproperties import Properties
from currency import get_supported_currencies, get_supported_historical_currencies, get_conversion_rate, get_historical_trend
from telebot import types
from tabulate import tabulate
from history import run as history_run
from flask import Flask, jsonify, request
from dotenv import load_dotenv
import os

load_dotenv()


configs = Properties()

with open("user.properties", "rb") as read_prop:
    configs.load(read_prop)

api_token = str(configs.get("api_token").data)

bot = telebot.TeleBot(api_token)

telebot.logger.setLevel(logging.INFO)

option = {}
user_list = {}

app = Flask(__name__)

# === Documentation of code.py ===

# Define listener for requests by user


def listener(user_requests):
    """
    listener(user_requests): Takes 1 argument user_requests and logs all user
    interaction with the bot including all bot commands run and any other issue logs.
    """
    for req in user_requests:
        if req.content_type == "text":
            print(
                "{} name:{} chat_id:{} \nmessage: {}\n".format(
                    str(datetime.now()),
                    str(req.chat.first_name),
                    str(req.chat.id),
                    str(req.text),
                )
            )

    message = (
        ("Sorry, I can't understand messages yet :/\n"
         "I can only understand commands that start with /. \n\n"
         "Type /faq or /help if you are stuck.")
    )

    try:
        helper.read_json()
        chat_id = user_requests[0].chat.id

        if user_requests[0].text[0] != "/":
            bot.send_message(chat_id, message)
    except Exception:
        pass


bot.set_update_listener(listener)


@bot.message_handler(commands=["chat"])
def command_chat(message):
    """
    Handles the /chat command
    """
    chat.run(message, bot)


@bot.message_handler(commands=["help"])
def show_help(m):

    helper.read_json()
    chat_id = m.chat.id

    message = "Here are the commands you can use: \n"
    commands = helper.getCommands()
    for c in commands:
        message += "/" + c + ", "
    message += "\nUse /menu for detailed instructions about these commands."
    bot.send_message(chat_id, message)


@bot.message_handler(commands=["faq"])
def faq(m):
    """
    Prints out the frequently asked questions for users to understand some common doubts. 
    Commands used to run this: command=['faq']
    """
    helper.read_json()
    chat_id = m.chat.id

    faq_message = (
        ('"What does this bot do?"\n'
         ">> DollarBot lets you manage your expenses so you can always stay on top of them! \n\n"
         '"How can I add an epxense?" \n'
         ">> Type /add, then select a category to type the expense. \n\n"
         '"Can I see history of my expenses?" \n'
         ">> Yes! Use /analytics to get a graphical display, or /history to view detailed summary.\n\n"
         '"I added an incorrect expense. How can I edit it?"\n'
         ">> Use /edit command. \n\n"
         '"Can I check if my expenses have exceeded budget?"\n'
         ">> Yes! Use /budget and then select the view category. \n\n")
    )
    bot.send_message(chat_id, faq_message)

# defines how the /start and /help commands have to be handled/processed


@bot.message_handler(commands=["start", "menu"])
def start_and_menu_command(m):
    """
    start_and_menu_command(m): Prints out the the main menu displaying the features that the
    bot offers and the corresponding commands to be run from the Telegram UI to use these features.
    Commands used to run this: commands=['start', 'menu']
    """
    helper.read_json()
    chat_id = m.chat.id

    text_intro = (
        ("Welcome to the Dollar Bot! \n"
         "DollarBot can track all your expenses with simple and easy to use commands :) \n"
         "Here is the complete menu. \n\n")
    )

    bot.send_message(chat_id, text_intro)
    commands = helper.getCommands()
    for c in commands:
        command_txt = ""
        # generate help text out of the commands dictionary defined at the top
        command_txt += "/" + c + ": "
        command_txt += commands[c] + "\n\n"
        bot.send_message(chat_id, command_txt)
    return True

# defines how the /add command has to be handled/processed


@bot.message_handler(commands=["add"])
def command_add(message):
    """
    command_add(message) Takes 1 argument message which contains the message from
    the user along with the chat ID of the user chat. It then calls add.py to run to execute
    the add functionality. Commands used to run this: commands=['add']
    """
    add.run(message, bot)

# handles group creation


@bot.message_handler(commands=["group"])
def command_group(message):
    """
    command_group(message): Take an argument message with content and chat ID. Calls group to 
    create a group for expense splitting. Commands to run this commands=["group"]
    """
    group.run(message, bot)

# defines how the /weekly command has to be handled/processed


@bot.message_handler(commands=["weekly"])
def command_weekly(message):
    """
    command_weekly(message) Takes 1 argument message which contains the message from
    the user along with the chat ID of the user chat. It then calls weekly.py to run to execute
    the weekly analysis functionality. Commands used to run this: commands=['weekly']
    """
    weekly.run(message, bot)

# defines how the /monthly command has to be handled/processed


@bot.message_handler(commands=["monthly"])
def command_monthly(message):
    """
    command_monthly(message) Takes 1 argument message which contains the message from
    the user along with the chat ID of the user chat. It then calls monthly.py to run to execute
    the monthly analysis functionality. Commands used to run this: commands=['monthly']
    """
    monthly.run(message, bot)

# handles add_recurring command


@bot.message_handler(commands=['add_recurring'])
def command_add_recurring(message):
    add_recurring.run(message, bot)

# handles pdf command


@bot.message_handler(commands=["pdf"])
def command_pdf(message):
    """
    command_history(message): Takes 1 argument message which contains the message from
    the user along with the chat ID of the user chat. It then calls pdf.py to run to execute
    the add functionality. Commands used to run this: commands=['pdf']
    """
    pdf.run(message, bot)

# handles updateCategory command


@bot.message_handler(commands=["updateCategory"])
def command_updateCategory(message):
    """
    command_updateCategory(message): Takes 1 argument message which contains the message from
    the user along with the chat ID of the user chat. It then calls updateCategory.py to run to execute
    the updateCategory functionality. Commands used to run this: commands=['updateCategory']
    """
    updateCategory.run(message, bot)

# function to fetch expenditure history of the user


@bot.message_handler(commands=["history"])
def command_history(message):
    """
    command_history(message): Takes 1 argument message which contains the message from
    the user along with the chat ID of the user chat. It then calls history.py to run to execute
    the add functionality. Commands used to run this: commands=['history']
    """
    history.run(message, bot)

# function to fetch expenditure history of the user


@bot.message_handler(commands=["sendEmail"])
def command_sendEmail(message):
    """
    command_history(message): Takes 1 argument message which contains the message from
    the user along with the chat ID of the user chat. It then calls sendEmail.py to run to execute
    the sending an email of the expense history. Commands used to run this: commands=['sendEmail']
    """
    sendEmail.run(message, bot)

# function to edit date, category or cost of a transaction


@bot.message_handler(commands=["edit"])
def command_edit(message):
    """
    command_edit(message): Takes 1 argument message which contains the message from
    the user along with the chat ID of the user chat. It then calls edit.py to run to execute
    the add functionality. Commands used to run this: commands=['edit']
    """
    edit.run(message, bot)

# function to display total expenditure


@bot.message_handler(commands=["display"])
def command_display(message):
    """
    command_display(message): Takes 1 argument message which contains the message from the user
    along with the chat ID of the user chat. It then calls display.py to run to execute the add functionality.
    Commands used to run this: commands=['display']
    """
    display.run(message, bot)

# function to estimate future expenditure


@bot.message_handler(commands=["estimate"])
def command_estimate(message):
    """
    command_estimate(message): Takes 1 argument message which contains the message from the user
    along with the chat ID of the user chat. It then calls delete.py to run to execute the add functionality.
    Commands used to run this: commands=['estimate']
    """
    estimate.run(message, bot)

# handles "/delete" command


@bot.message_handler(commands=["delete"])
def command_delete(message):
    """
    command_delete(message): Takes 1 argument message which contains the message from the user
    along with the chat ID of the user chat. It then calls delete.py to run to execute the add functionality.
    Commands used to run this: commands=['display']
    """
    delete.run(message, bot)


@bot.message_handler(commands=["delete"])
def command_delete(message):
    """
    command_delete(message): Takes 1 argument message which contains the message from the user
    along with the chat ID of the user chat. It then calls delete.py to run to execute the add functionality.
    Commands used to run this: commands=['delete']
    """
    delete.run(message, bot)

# handles "/view_credit" command


@bot.message_handler(commands=["view_credit"])
def command_view_credit(message):
    """
    command_view_credit(message): Takes 1 argument message which contains the message from the user
    along with the chat ID of the user chat. It then calls credit_view.py to run to view the credit record
    Commands used to run this: commands=['view_credit']
    """
    credit_view.run(message, bot)

# handles "/setup_credit" command


@bot.message_handler(commands=["setup_credit"])
def command_setup_credit(message):
    """
    command_setup_credit(message): Takes 1 argument message which contains the message from the user
    along with the chat ID of the user chat. It then calls credit_setup.py to run to add a new credit account
    Commands used to run this: commands=['view_credit']
    """
    credit_setup.run(message, bot)

# handles "/pay_credit" command


@bot.message_handler(commands=["pay_credit"])
def command_pay_credit(message):
    """
    command_pay_credit(message): Takes 1 argument message which contains the message from the user
    along with the chat ID of the user chat. It then calls credit_pay.py to run to pay off a credit
    account
    Commands used to run this: commands=['pay_credit']
    """
    credit_pay.run(message, bot)

# handles "/clear_credit" command


@bot.message_handler(commands=["clear_credit"])
def command_clear_credit(message):
    """
    command_clear_credit(message): Takes 1 argument message which contains the message from the user
    along with the chat ID of the user chat. It then calls credit_clear.py to run to clear expenses
    for a credit account
    Commands used to run this: commands=['clear_credit']
    """
    credit_clear.run(message, bot)

# handles "/delete_credit" command


@bot.message_handler(commands=["delete_credit"])
def command_delete_credit(message):
    """
    command_delete_credit(message): Takes 1 argument message which contains the message from the user
    along with the chat ID of the user chat. It then calls credit_delete.py to run to delete a credit
    account.
    Commands used to run this: commands=['delete_credit']
    """
    credit_delete.run(message, bot)


@bot.message_handler(commands=["setup_credit_calendar"])
def command_setup_credit_calendar(message):
    """
    command_setup_credit_calendar(message): Takes 1 argument message which contains the message from the user
    along with the chat ID of the user chat. It then calls creddit_calendar.py to run to add a due date
    to a credit account for a users google calendar
    Commands used to run this: commands=['setup_credit_calendar']
    """
    credit_calendar.run(message, bot)


# handles budget command
@bot.message_handler(commands=["budget"])
def command_budget(message):
    """
    Takes 1 argument message which contains the message from the user 
    along with the chat ID of the user chat. It then calls budget.py to 
    execute the budget functionality. Commands used to run this: command=['budget']
    """
    budget.run(message, bot)

# handles analytics command


@bot.message_handler(commands=["analytics"])
def command_analytics(message):
    """
    command_analytics(message): Take an argument message with content and chat ID. Calls analytics to 
    run analytics. Commands to run this commands=["analytics"]
    """
    analytics.run(message, bot)

# handles predict command


@bot.message_handler(commands=["predict"])
def command_predict(message):
    """
    command_predict(message): Take an argument message with content and chat ID. Calls predict to 
    analyze budget and spending trends and suggest a future budget. Commands to run this commands=["predict"]
    """
    predict.run(message, bot)


@bot.message_handler(commands=['currency'])
def show_supported_currencies(message):
    """
    Sends a message listing all the supported currencies when the user types /currency.
    """
    chat_id = message.chat.id
    supported_currencies = get_supported_currencies()

    if supported_currencies:
        currency_list = ", ".join(supported_currencies)
        bot.send_message(chat_id, f"Supported Currencies: {currency_list}")
    else:
        bot.send_message(
            chat_id, "Failed to fetch supported currencies. Please try again later.")


@bot.message_handler(commands=['convert'])
def convert_currency(message):
    """
    Converts the specified currency to USD when the user types /convert <currency>.
    """
    chat_id = message.chat.id
    try:
        # Expect the message format to be like "/convert CNY to USD"
        text = message.text.split()
        if len(text) != 4 or text[1].upper() == 'USD' or text[3].upper() != 'USD':
            bot.send_message(
                chat_id, "Usage: /convert <currency_code> to USD (e.g., /convert EUR to USD)")
            return

        base_currency = text[1].upper()

        # Fetch the conversion rate using the function from currency.py
        conversion_rate = get_conversion_rate(base_currency, 'USD')

        if conversion_rate:
            bot.send_message(
                chat_id, f"1 {base_currency} = {conversion_rate} USD")
        else:
            bot.send_message(
                chat_id, "Failed to fetch the conversion rate. Please ensure the currency code is valid.")
    except Exception as e:
        print(f"Error processing conversion command: {e}")
        bot.send_message(chat_id, "An error occurred. Please try again.")


@bot.message_handler(commands=['currencycalculator'])
def start_currency_calculator(message):
    """
    Initiates the currency calculator by asking the user to choose the base currency.
    """
    chat_id = message.chat.id
    supported_currencies = get_supported_currencies()

    if supported_currencies:
        # Create a ReplyKeyboardMarkup to display currency options
        markup = types.ReplyKeyboardMarkup(
            one_time_keyboard=True, resize_keyboard=True)
        for currency in supported_currencies:
            markup.add(currency)
        msg = bot.reply_to(
            message, "Select the currency you want to convert from:", reply_markup=markup)
        bot.register_next_step_handler(msg, get_target_currency)
    else:
        bot.send_message(
            chat_id, "Failed to fetch supported currencies. Please try again later.")


@bot.message_handler(commands=['portfolio'])
def start_portfolio(message):
    """
    Initiates the portfolio service by asking the user to choose an action.
    """
    portfolio.run(message, bot)


@bot.message_handler(commands=['portfolio'])
def start_portfolio(message):
    """
    Initiates the portfolio service by asking the user to choose an action.
    """
    portfolio.run(message, bot)


@bot.message_handler(commands=['historicaltrends'])
def currency_historical_trends(message):
    """
    Initiates the historical plots by asking users what currency they would like to use
    """
    chat_id = message.chat.id
    supported_currencies = get_supported_historical_currencies()

    currencies = types.ReplyKeyboardMarkup(
        one_time_keyboard=True, resize_keyboard=True)
    for currency in supported_currencies:
        currencies.add(currency)
    msg = bot.reply_to(
        message, "Select the first currency you want to collect historical data from", reply_markup=currencies)
    bot.register_next_step_handler(msg, get_target_historical_currency)


def get_target_currency(message):
    """
    Asks the user to select the target currency for conversion.
    """
    chat_id = message.chat.id
    base_currency = message.text.upper()

    # Store the base currency in user context
    user_data = helper.read_json()
    if str(chat_id) not in user_data:
        user_data[str(chat_id)] = helper.createNewUserRecord()
    user_data[str(chat_id)]['base_currency'] = base_currency
    helper.write_json(user_data)

    # Fetch supported currencies again to display the options for the target currency
    supported_currencies = get_supported_currencies()

    if supported_currencies:
        markup = types.ReplyKeyboardMarkup(
            one_time_keyboard=True, resize_keyboard=True)
        for currency in supported_currencies:
            # Ensure the target currency is not the same as the base currency
            if currency != base_currency:
                markup.add(currency)
        msg = bot.reply_to(
            message, "Select the currency you want to convert to:", reply_markup=markup)
        bot.register_next_step_handler(msg, get_amount_to_convert)
    else:
        bot.send_message(
            chat_id, "Failed to fetch supported currencies. Please try again later.")


def get_target_historical_currency(message):
    """
    Gets the type of currency user would like to use
    """
    chat_id = message.chat.id
    selected_currency = message.text.upper()

    # Store the base currency in user context
    user_data = helper.read_json()
    if str(chat_id) not in user_data:
        user_data[str(chat_id)] = helper.createNewUserRecord()
    user_data[str(chat_id)]['selected_currency_1'] = selected_currency
    helper.write_json(user_data)

    # Fetch supported currencies again to display the options for the target currency
    supported_currencies = get_supported_historical_currencies()
    currencies = types.ReplyKeyboardMarkup(
        one_time_keyboard=True, resize_keyboard=True)
    for currency in supported_currencies:
        # Ensure the target currency is not the same as the base currency
        if currency != selected_currency:
            currencies.add(currency)

    msg = bot.reply_to(
        message, "Select the currency you want to compare to", reply_markup=currencies)
    bot.register_next_step_handler(msg, get_years_to_go_back)


def get_years_to_go_back(message):
    """
    Asks the user to input the amount of years to go back
    """
    chat_id = message.chat.id
    selected_currency = message.text.upper()

    # Save the target currency in user context
    user_data = helper.read_json()
    user_data[str(chat_id)]['selected_currency_2'] = selected_currency
    helper.write_json(user_data)
    years = types.ReplyKeyboardMarkup(
        one_time_keyboard=True, resize_keyboard=True)
    for i in range(1, 11):
        years.add(str(i))
    msg = bot.send_message(
        chat_id, "How many years would you like the data to go back: ", reply_markup=years)
    bot.register_next_step_handler(msg, create_historical_plots)


def create_historical_plots(message):
    """
    Creates the historical plots from the two currencies selected
    and posts them to user
    """
    chat_id = message.chat.id
    years = int(message.text)
    user_data = helper.read_json()
    selected_currency_1 = user_data.get(
        str(chat_id), {}).get('selected_currency_1', None)
    selected_currency_2 = user_data.get(
        str(chat_id), {}).get('selected_currency_2', None)

    if not selected_currency_1 or not selected_currency_2:
        bot.send_message(chat_id, "Error when creating plots")
        return

    trend1 = get_historical_trend(selected_currency_1, years)
    trend2 = get_historical_trend(selected_currency_2, years)

    plt.plot(trend1, color='blue')
    plt.plot(trend2, color='green', linestyle="--")
    plt.xticks(fontsize=8)
    plt.xlabel("Time")
    plt.ylabel("to 1 USD Exchange Rate")
    plt.legend([selected_currency_1, selected_currency_2])

    plt.savefig("plot.png")
    plt.close()

    with open('plot.png', 'rb') as photo:
        bot.send_photo(chat_id=chat_id, photo=photo)


def get_amount_to_convert(message):
    """
    Asks the user to input the amount to convert.
    """
    chat_id = message.chat.id
    target_currency = message.text.upper()

    # Save the target currency in user context
    user_data = helper.read_json()
    user_data[str(chat_id)]['target_currency'] = target_currency
    helper.write_json(user_data)

    # Ask the user to enter the amount
    msg = bot.send_message(
        chat_id, f"Enter the amount in {user_data[str(chat_id)]['base_currency']} you want to convert to {target_currency}:")
    bot.register_next_step_handler(msg, perform_currency_conversion)


def perform_currency_conversion(message):
    """
    Performs the currency conversion between the selected base and target currencies.
    """
    chat_id = message.chat.id
    user_data = helper.read_json()
    base_currency = user_data.get(str(chat_id), {}).get('base_currency', 'USD')
    target_currency = user_data.get(
        str(chat_id), {}).get('target_currency', 'USD')

    try:
        amount = float(message.text)

        # Fetch the conversion rate using the function from currency.py
        conversion_rate = get_conversion_rate(base_currency, target_currency)

        if conversion_rate:
            converted_amount = round(amount * conversion_rate, 2)
            bot.send_message(
                chat_id, f"{amount} {base_currency} = {converted_amount} {target_currency}")
        else:
            bot.send_message(
                chat_id, "Failed to fetch the conversion rate. Please try again.")
    except ValueError:
        bot.send_message(
            chat_id, "Invalid input. Please enter a numeric value.")
    except Exception as e:
        print(f"Error during conversion: {e}")
        bot.send_message(chat_id, "An error occurred. Please try again.")


@app.route('/')
def home():
    """
    The default message for the flask development server
    """
    return 'Flask is running!'


@app.route('/oauth2callback')
def oauth2callback():
    """
    Route for setting up the oauth token. Downloads it into
    oauth_record.json
    """
    # Extract the authorization code and chat_id
    try:
        auth_code = request.args.get('code')
        chat_id = request.args.get('state')
        CLIENT_ID = os.getenv("CLIENT_ID", "")
        CLIENT_SECRET = os.getenv("CLIENT_SECRET", "")
        # Exchange the authorization code for an access token
        token_url = "https://oauth2.googleapis.com/token"
        token_data = {
            'code': auth_code,
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'grant_type': 'authorization_code',
            'redirect_uri': 'http://localhost:5000/oauth2callback'
        }
        token_response = requests.post(token_url, data=token_data)
        token_info = token_response.json()
        oauth_record = helper.read_oauth_json()
        oauth_record[chat_id] = {}
        oauth_record[chat_id]["access_token"] = token_info['access_token']
        expiration_time = datetime.utcnow(
        ) + timedelta(seconds=token_info['expires_in'])
        oauth_record[chat_id]["expires"] = expiration_time.timestamp()
        helper.write_oauth_json(oauth_record)
        return jsonify({"message": "Successfully created your token, please return to the app."}), 200
    except Exception as e:
        logging.exception(str(e))
        return jsonify({"message": "something went wrong, try again later."}), 400


def run_flask():
    """
    Runs the flask application for handling oauth and calendar setup.
    This allows for future implementations of google api items.
    This process is on an alternate thread
    """
    app.run(debug=False, use_reloader=False, threaded=True)


shutdown_event = threading.Event()


def main():
    """
    main() The entire bot's execution begins here. It ensure the bot variable begins
    polling and actively listening for requests from telegram. It also sets up a 
    flask server for the oauth
    """
    try:
        flask_thread = threading.Thread(target=run_flask, daemon=True)
        flask_thread.start()
        bot.polling(none_stop=True)
    except KeyboardInterrupt:
        logging.info("Shutdown requested. Stopping threads...")
        shutdown_event.set()
    except Exception as e:
        logging.exception(str(e))
        time.sleep(3)
        print("Connection Timeout")
    finally:
        # Ensure Flask thread stops when the bot exits
        flask_thread.join(timeout=1)
        logging.info("Flask app stopped.")


if __name__ == "__main__":
    main()

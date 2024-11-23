"""
File: portfolio_sell.py
Author: Nathan Lorenc
Date: November 22, 2024
Description: File contains functionality for selling stocks.
"""
import helper
import logging
import yfinance as yf
import csv
from telebot import types

# === Documentation of portfolio_buy.py ===


def run(message, bot):
    """
    run(message, bot): This is the main function used to implement the budget delete feature.
    It takes 2 arguments for processing - message which is the message from the user, and bot
    which is the telegram bot object from the main code.py function. It gets the user's chat ID
    from the message object, and reads all user data through the read_json method from the helper module.
    It then proceeds to empty the budget data for the particular user based on the user ID provided from the UI.
    It returns a simple message indicating that this operation has been done to the UI.
    """
    chat_id = message.chat.id
    msg = bot.send_message(chat_id, "Enter a Stock Ticker")
    bot.register_next_step_handler(msg, handle_stock_name, bot)


def handle_stock_name(message, bot):
    """
    Handles ensuring that the stock name is for a valid stock.
    """
    chat_id = message.chat.id
    ticker = message.text.upper()

    # Check to see if the stock is real, and get its price if it is
    stock = yf.Ticker(ticker)
    if stock is not None:
        msg = bot.send_message(chat_id, "Enter Number of Shares")
        bot.register_next_step_handler(
            msg, handle_stock_sell, bot, ticker, stock)
    else:
        bot.send_message(chat_id, "Invalid Stock")


def handle_stock_sell(message, bot, ticker, stock):
    """
    Performs the stock sale and retrieves the current stock price.
    """
    try:
        chat_id = message.chat.id
        shares = int(message.text)
        price = stock.info['currentPrice']
        record = edit_user_record(chat_id, bot, ticker, shares, price)
        if record is None:
            return False
        helper.write_portfolio_json(record)
        return True
    except Exception as e:
        bot.send_message(chat_id, "Oh no!")
        print(e)


def edit_user_record(chat_id, bot, ticker, shares, price):
    """
    Stores the stock purchase for the user.
    """
    user_list = helper.read_portfolio_json()
    if user_list is None:
        return None
    if str(chat_id) not in user_list:
        return None

    curr_portfolio = user_list[str(chat_id)]["stocks"]
    found = False
    saleSuccess = False
    prevStock = None
    csv_portfolio = csv.reader(curr_portfolio)
    for stock in csv_portfolio:
        if not found and stock[0] == ticker:
            if int(stock[1]) < shares:
                found = True
                break
            elif int(stock[1]) == shares:
                prevStock = stock
                rem_stock = "{},{},{}".format(stock[0], stock[1], stock[2])
                curr_portfolio.remove(rem_stock)
                found = True
                saleSuccess = True
                break
            else:
                prevStock = stock
                rem_stock = "{},{},{}".format(stock[0], stock[1], stock[2])
                curr_portfolio.remove(rem_stock)
                prevStock[1] = int(prevStock[1])
                prevStock[1] -= shares
                prevStockString = "{},{},{}".format(
                    prevStock[0], prevStock[1], prevStock[2])
                curr_portfolio.append(prevStockString)
                found = True
                saleSuccess = True
                break

    if saleSuccess:
        profit = (price - float(prevStock[2])) * shares
        bot.send_message(
            chat_id,
            """
            You have sold {} shares of {} for ${} per share
            """.format(
                shares, ticker, price
            ),
        )
        bot.send_message(
            chat_id, "You have made a profit of ${:.2f}".format(profit))
        user_list[str(chat_id)]["stocks"] = curr_portfolio
        return user_list
    else:
        bot.send_message(
            chat_id, "You don't have enough shares to make this sale")
        return None

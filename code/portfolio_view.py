"""
File: portfolio_view.py
Author: Nathan Lorenc
Date: November 22, 2024
Description: File contains functionality for viewing one's portfolio.
"""
import helper
import yfinance as yf
from tabulate import tabulate
import csv


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
    bot.send_message(chat_id, "Here is your Portfolio:")
    viewPortfolioTable(message, bot)


def viewPortfolioTable(message, bot):
    """
    Display portfolio in a tabular format for the user.
    """
    chat_id = message.chat.id
    user_list = helper.read_portfolio_json()
    if user_list is None:
        bot.send_message(chat_id, "You don't own any stocks")
        return False
    elif user_list.get(str(chat_id), None) is None:
        return False
    elif not user_list[str(chat_id)]["stocks"]:
        return False
    else:
        portfolio = user_list[str(chat_id)]["stocks"]
        table = [["Stock", "Shares", "Buy Price",
                  "Current Price", "Percent Change"]]
        portfolio_csv = csv.reader(portfolio)
        portfolio_worth = 0
        for stock in portfolio_csv:
            ticker = yf.Ticker(stock[0])
            curr_price = ticker.info['currentPrice']
            curr_price = round(curr_price, 2)
            percent_change = ((curr_price / float(stock[2])) - 1.0) * 100
            percent_change = round(percent_change, 2)
            portfolio_worth += int(stock[1]) * curr_price
            table.append([stock[0], stock[1], "$ " + stock[2],
                          "$ " + str(curr_price), str(percent_change) + "%"])
        bot.send_message(
            chat_id, "Your portfolio is worth ${:.2f}".format(portfolio_worth))
        portfolio_table = "<pre>" + \
            tabulate(table, headers='firstrow')+"</pre>"
        bot.send_message(chat_id, portfolio_table, parse_mode="HTML")
        return True

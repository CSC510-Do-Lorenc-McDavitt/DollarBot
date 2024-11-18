"""
File: portfolio.py
Author: Nathan Lorenc
Date: November 13, 2024
Description: File contains functionality for retrieving
stock portfolio prices for the user.
"""
import helper
import portfolio_buy
import portfolio_sell
import logging
from telebot import types
import yfinance as yf
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from tabulate import tabulate
import csv

def run(message, bot):
    """
    run(message, bot): This is the main function used to implement the portfolio feature.
    It pop ups a menu on the bot asking the user to choose to buy a stock, sell a stock, or view
    their portfolio in various ways, after which control is given to post_operation_selection(message, bot) 
    for further proccessing. It takes 2 arguments for processing - message which is the message 
    from the user, and bot which is the telegram bot object from the main code.py function.
    """
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    options = helper.getPortfolioOptions()
    markup.row_width = 2
    for c in options.values():
        markup.add(c)
    msg = bot.reply_to(message, "Select Operation", reply_markup=markup)
    bot.register_next_step_handler(msg, post_operation_selection, bot)

def post_operation_selection(message, bot):
    """
    post_operation_selection(message, bot): It takes 2 arguments for processing - message which
    is the message from the user, and bot which is the telegram bot object from the
    run(message, bot): function in the portfolio.py file. Depending on the action chosen by the user,
    it passes on control to the corresponding functions which are all located in different files.
    """
    try:
        chat_id = message.chat.id
        op = message.text
        options = helper.getPortfolioOptions()
        if op not in options.values():
            bot.send_message(
                chat_id, "Invalid", reply_markup=types.ReplyKeyboardRemove()
            )
            raise Exception('Sorry I don\'t recognise this operation "{}"!'.format(op))
        if op == options["buy"]:
            portfolio_buy.run(message, bot)
        elif op == options["sell"]:
            portfolio_sell.run(message, bot)
        elif op == options["viewTable"]:
            viewPortfolioTable(message, bot)
    except Exception as e:
        helper.throw_exception(e, message, bot, logging)

def viewPortfolioTable(message, bot):
    chat_id = message.chat.id
    user_list = helper.read_portfolio_json()
    if user_list is None:
        bot.send_message(chat_id, "You don't own any stocks")
    else:
        portfolio = user_list[str(chat_id)]["stocks"]
        table = [["Stock", "Shares", "Buy Price", "Current Price", "Percent Change"]]
        portfolio_csv = csv.reader(portfolio)
        portfolio_worth = 0
        for stock in portfolio_csv:
            ticker = yf.Ticker(stock[0])
            curr_price = ticker.info['currentPrice']
            percent_change = (curr_price / float(stock[2])) - 1.0
            percent_change = round(percent_change, 2)
            portfolio_worth += int(stock[1]) * curr_price
            table.append([stock[0], stock[1], "$ " + stock[2], 
                          "$ " + str(curr_price), str(percent_change) + "%"])
        bot.send_message(chat_id, "Your portfolio is worth ${}".format(portfolio_worth))
        portfolio_table = "<pre>"+ tabulate(table, headers='firstrow')+"</pre>"
        bot.send_message(chat_id, portfolio_table, parse_mode="HTML")

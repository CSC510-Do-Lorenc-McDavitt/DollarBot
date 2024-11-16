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
        # elif op == options["sell"]:
        #     portfolio_sell.run(message, bot)

        # elif op == options["viewTable"]:
        #     budget_delete.run(message, bot)
        # elif op == options["viewGraphWeek"]:
        #     budget_delete.run(message, bot)
        # elif op == options["viewGraphMonth"]:
        #     budget_delete.run(message, bot)
        # elif op == options["viewGraphYear"]:
        #     budget_delete.run(message, bot)
    except Exception as e:
        helper.throw_exception(e, message, bot, logging)


def buyStock(stock: str, numShares: int, pricePerShare: float):
    ticker = yf.Ticker(stock)
    print(ticker.history(period="1mo"))
    return 0

def sellStock(stock: str, numShares: int):
    return 0

def viewPortfolioTable():
    return 0

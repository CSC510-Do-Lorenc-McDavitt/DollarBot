import helper
import logging
import yfinance as yf
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
    chat_id = message.chat.id
    ticker = message.text.upper()

    # Check to see if the stock is real, and get its price if it is
    stock = yf.Ticker(ticker)
    if stock is not None:
        msg = bot.send_message(chat_id, "Enter Number of Shares")
        bot.register_next_step_handler(msg, handle_stock_buy, bot, ticker, stock)
    else:
        bot.send_message(chat_id, "Invalid Stock")

def handle_stock_buy(message, bot, ticker, stock):
    chat_id = message.chat.id
    shares = int(message.text)
    price = stock.info['currentPrice']
    helper.write_portfolio_json(
        add_user_record(
            chat_id, "{},{},{}".format(ticker, shares, price)
        )
    )
    bot.send_message(
        chat_id, 
        """
        You have bought {} shares of {} for ${} per share
        """.format(
            shares, ticker, price
        ),
    )

def add_user_record(chat_id, record_to_be_added):
    """
    Stores the stock purchase for the user.
    """
    user_list = helper.read_portfolio_json()
    if user_list is None:
        user_list = {}
    if str(chat_id) not in user_list:
        user_list[str(chat_id)] = helper.createNewPortfolioUserRecord()

    user_list[str(chat_id)]["stocks"].append(record_to_be_added)
    return user_list

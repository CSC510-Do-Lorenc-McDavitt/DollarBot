import os
import json
import portfolio_buy
from mock.mock import patch
from mock import ANY
import yfinance as yf
from telebot import types

@patch("telebot.telebot")
def test_buy_MSFT(mock_telebot, mocker):
    MOCK_USER_DATA = test_read_portfolio_json()
    mocker.patch.object(portfolio_buy, "helper")
    portfolio_buy.helper.read_portfolio_json.return_value = MOCK_USER_DATA
    mc = mock_telebot.return_value
    message = create_message("MSFT")
    message.text = "MSFT"
    message.chat.id = 555
    portfolio_buy.handle_stock_name(message, mc)
    assert mc.send_message_called
    mc.send_message.assert_called_once_with(555, "Enter Number of Shares")

@patch("telebot.telebot")
def test_buy_invalid_blank(mock_telebot, mocker):
    MOCK_USER_DATA = test_read_portfolio_json()
    mocker.patch.object(portfolio_buy, "helper")
    portfolio_buy.helper.read_portfolio_json.return_value = MOCK_USER_DATA
    mc = mock_telebot.return_value
    message = create_message("")
    message.text = ""
    portfolio_buy.handle_stock_name(message, mc)
    assert mc.send_message_called

@patch("telebot.telebot")
def test_buy_15_MSFT(mock_telebot, mocker):
    MOCK_USER_DATA = test_read_portfolio_json()
    mocker.patch.object(portfolio_buy, "helper")
    portfolio_buy.helper.read_portfolio_json.return_value = MOCK_USER_DATA
    mc = mock_telebot.return_value
    ticker = 'MSFT'
    message = create_message("15")
    message.text = "15"
    message.chat.id = 12345
    stock = yf.Ticker(ticker)
    portfolio_buy.handle_stock_buy(message, mc, ticker, stock)
    assert mc.send_message_called

@patch("telebot.telebot")
def test_buy_more_MSFT(mock_telebot, mocker):
    MOCK_USER_DATA = test_read_portfolio_json()
    mocker.patch.object(portfolio_buy, "helper")
    portfolio_buy.helper.read_portfolio_json.return_value = MOCK_USER_DATA
    mc = mock_telebot.return_value
    ticker = 'MSFT'
    message = create_message("15")
    message.text = "15"
    message.chat.id = 555
    stock = yf.Ticker(ticker)
    portfolio_buy.handle_stock_buy(message, mc, ticker, stock)
    assert mc.send_message_called

@patch("telebot.telebot")
def test_buy_AAPL(mock_telebot, mocker):
    MOCK_USER_DATA = test_read_portfolio_json()
    mocker.patch.object(portfolio_buy, "helper")
    portfolio_buy.helper.read_portfolio_json.return_value = MOCK_USER_DATA
    mc = mock_telebot.return_value
    ticker = 'AAPL'
    message = create_message("20")
    message.text = "20"
    message.chat.id = 12345
    stock = yf.Ticker(ticker)
    portfolio_buy.handle_stock_buy(message, mc, ticker, stock)
    assert mc.send_message_called

@patch("telebot.telebot")
def test_buy_RDDT(mock_telebot, mocker):
    MOCK_USER_DATA = test_read_portfolio_json()
    mocker.patch.object(portfolio_buy, "helper")
    portfolio_buy.helper.read_portfolio_json.return_value = MOCK_USER_DATA
    mc = mock_telebot.return_value
    ticker = 'RDDT'
    message = create_message("30")
    message.text = "30"
    message.chat.id = 12345
    stock = yf.Ticker(ticker)
    portfolio_buy.handle_stock_buy(message, mc, ticker, stock)
    assert mc.send_message_called

@patch("telebot.telebot")
def test_buy_NVDA(mock_telebot, mocker):
    MOCK_USER_DATA = test_read_portfolio_json()
    mocker.patch.object(portfolio_buy, "helper")
    portfolio_buy.helper.read_portfolio_json.return_value = MOCK_USER_DATA
    mc = mock_telebot.return_value
    ticker = 'NVDA'
    message = create_message("1000")
    message.text = "1000"
    message.chat.id = 12345
    stock = yf.Ticker(ticker)
    portfolio_buy.handle_stock_buy(message, mc, ticker, stock)
    assert mc.send_message_called

def test_read_portfolio_json():
    try:
        if not os.path.exists("./test/dummy_portfolio.json"):
            with open("./test/dummy_portfolio.json", "w", encoding="utf-8") as json_file:
                json_file.write("{}")
            return json.dumps("{}")
        elif os.stat("./test/dummy_portfolio.json").st_size != 0:
            with open("./test/dummy_portfolio.json", encoding="utf-8") as portfolio:
                portfolio_data = json.load(portfolio)
            return portfolio_data

    except FileNotFoundError:
        print("---------NO PORTFOLIO FOUND---------")

def create_message(text):
    params = {"messagebody": text}
    chat = types.User(11, False, "test")
    return types.Message(1, None, None, chat, "text", params, "")

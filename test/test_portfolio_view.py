import os
import json
import portfolio_view
from mock.mock import patch
from telebot import types

@patch("telebot.telebot")
def test_view_portfolio_passing(mock_telebot, mocker):
    MOCK_USER_DATA = test_read_portfolio_json()
    mocker.patch.object(portfolio_view, "helper")
    portfolio_view.helper.read_portfolio_json.return_value = MOCK_USER_DATA
    mc = mock_telebot.return_value
    message = create_message("hello from portfolio_view test run!")
    message.chat.id = 555
    assert portfolio_view.viewPortfolioTable(message, mc)

@patch("telebot.telebot")
def test_view_portfolio_empty(mock_telebot, mocker):
    MOCK_USER_DATA = test_read_portfolio_json()
    mocker.patch.object(portfolio_view, "helper")
    portfolio_view.helper.read_portfolio_json.return_value = MOCK_USER_DATA
    mc = mock_telebot.return_value
    message = create_message("hello from portfolio_view test run!")
    message.chat.id = 623
    assert not portfolio_view.viewPortfolioTable(message, mc)

@patch("telebot.telebot")
def test_view_portfolio_nonexistent(mock_telebot, mocker):
    MOCK_USER_DATA = test_read_portfolio_json()
    mocker.patch.object(portfolio_view, "helper")
    portfolio_view.helper.read_portfolio_json.return_value = MOCK_USER_DATA
    mc = mock_telebot.return_value
    message = create_message("hello from portfolio_view test run!")
    message.chat.id = 0
    assert not portfolio_view.viewPortfolioTable(message, mc)

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

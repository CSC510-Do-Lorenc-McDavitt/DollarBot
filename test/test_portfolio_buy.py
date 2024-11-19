import portfolio_buy
from mock.mock import patch
from telebot import types

def test_buy_valid_stock():
    assert False

def test_buy_invalid_stock():
    assert False

def test_buy_invalid_amount():
    assert False

def test_buy_more():
    "Tests buying more of an existing stock holding"
    assert False

def create_message(text):
    params = {"messagebody": text}
    chat = types.User(11, False, "test")
    message = types.Message(1, None, None, chat, "text", params, "")
    message.text = text
    return message

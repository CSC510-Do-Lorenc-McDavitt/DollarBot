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

def test_read_portfolio_json():
    try:
        if not os.path.exists("./test/dummy_portfolio.json"):
            with open("./test/dummy_portfolio.json", "w", encoding="utf-8") as json_file:
                json_file.write("{}")
            return json.dumps("{}")
        elif os.stat("./test/dummy_portfolio.json").st_size != 0:
            with open("portfolio.json", encoding="utf-8") as portfolio:
                portfolio_data = json.load(portfolio)
            return portfolio_data

    except FileNotFoundError:
        print("---------NO PORTFOLIO FOUND---------")


def create_message(text):
    params = {"messagebody": text}
    chat = types.User(11, False, "test")
    message = types.Message(1, None, None, chat, "text", params, "")
    message.text = text
    return message

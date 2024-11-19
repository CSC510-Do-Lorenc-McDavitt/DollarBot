import os
import json
# from code import portfolio_view
# from mock.mock import patch
# from telebot import types

# def test_view_portfolio_passing(mock_telebot, mocker):
#     mc = mock_telebot.return_value
#     mc.send_message.return_value = True
#     mocker.patch.object(portfolio_view, "helper")

#     assert False

# def test_view_portfolio_empty(mock_telebot, mocker):
#     assert False

# def test_view_portfolio_nonexistent(mock_telebot, mocker):
#     assert False

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

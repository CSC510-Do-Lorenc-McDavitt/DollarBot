import mock
from mock.mock import patch
from telebot import types
import portfolio

@patch("telebot.telebot")
def test_run(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mc.reply_to.return_value = True
    message = create_message("hello from test run!")
    portfolio.run(message, mc)
    assert mc.reply_to_called

@patch("telebot.telebot")
def test_post_operation_selection_failing_case(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mc.send_message.return_value = True

    mocker.patch.object(portfolio, "helper")
    portfolio.helper.getPortfolioOptions.return_value = {}

    message = create_message("hello from portfolio test run!")
    portfolio.post_operation_selection(message, mc)
    mc.send_message.assert_called_with(11, "Invalid", reply_markup=mock.ANY)

@patch("telebot.telebot")
def test_post_operation_selection_buy_case(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mc.send_message.return_value = True

    mocker.patch.object(portfolio, "portfolio_buy")
    portfolio.portfolio_buy.run.return_value = True

    mocker.patch.object(portfolio, "helper")
    portfolio.helper.getPortfolioOptions.return_value = {
        "buy": "Buy a Stock",
        "sell": "Sell a Stock",
        "view": "View Portfolio",
    }

    message = create_message("Buy a Stock")
    portfolio.post_operation_selection(message, mc)
    assert portfolio.portfolio_buy.run.called

@patch("telebot.telebot")
def test_post_operation_selection_sell_case(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mc.send_message.return_value = True

    mocker.patch.object(portfolio, "portfolio_sell")
    portfolio.portfolio_sell.run.return_value = True

    mocker.patch.object(portfolio, "helper")
    portfolio.helper.getPortfolioOptions.return_value = {
        "buy": "Buy a Stock",
        "sell": "Sell a Stock",
        "view": "View Portfolio",
    }

    message = create_message("Sell a Stock")
    portfolio.post_operation_selection(message, mc)
    assert portfolio.portfolio_sell.run.called

@patch("telebot.telebot")
def test_post_operation_selection_view_case(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mc.send_message.return_value = True

    mocker.patch.object(portfolio, "portfolio_view")
    portfolio.portfolio_view.run.return_value = True

    mocker.patch.object(portfolio, "helper")
    portfolio.helper.getPortfolioOptions.return_value = {
        "buy": "Buy a Stock",
        "sell": "Sell a Stock",
        "view": "View Portfolio",
    }

    message = create_message("View Portfolio")
    portfolio.post_operation_selection(message, mc)
    assert portfolio.portfolio_view.run.called

def create_message(text):
    params = {"messagebody": text}
    chat = types.User(11, False, "test")
    message = types.Message(1, None, None, chat, "text", params, "")
    message.text = text
    return message

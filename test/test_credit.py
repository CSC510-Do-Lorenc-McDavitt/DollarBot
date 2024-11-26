import os
import json
from mock.mock import patch
from telebot import types
import credit_clear
import credit_delete
import credit_pay
import credit_view
import credit_setup
import credit_calendar

from mock import ANY, call
from datetime import datetime

dateFormat = "%d-%b-%Y"
timeFormat = "%H:%M"
monthFormat = "%b-%Y"
date = datetime.today().date()

sample_data = {}

def setUp():
  # Code to run before each test method
  global sample_data
  sample_data = {
    "12345":{
        "account 1": {
            "expenses": [
                "21-Aug-2024,Food,200.0",
                "17-Nov-2024,Food,10.0",
                "17-Dec-2024,Food,10.0",
                "17-Jan-2025,Food,10.0",
                "17-Feb-2025,Food,10.0",
                "17-Mar-2025,Food,10.0",
                "16-Jul-2024,Groceries,40.0"
            ],
            "due date": 5,
            "owe": 900.0,
            "calendar": False
        }
    }
}


@patch("telebot.telebot")
def test_view_credit(mock_telebot, mocker):
    setUp()
    mc = mock_telebot.return_value
    mc.send_message.return_value = True
    mocker.patch.object(credit_view, "helper")
    credit_view.helper.read_credit_json.return_value = sample_data

    message = create_message("sample")
    message.chat.id = 12345
    credit_view.run(message, mc)
    assert mc.send_message.call_args_list[0] == call(12345, "Showing Accounts and Credit Expenses:\n------------------------------------------------------\naccount 1\n  Expenses\n    21-Aug-2024,Food,200.0\n    17-Nov-2024,Food,10.0\n    17-Dec-2024,Food,10.0\n    17-Jan-2025,Food,10.0\n    17-Feb-2025,Food,10.0\n    17-Mar-2025,Food,10.0\n    16-Jul-2024,Groceries,40.0\n  Monthly Due Date: 5\n  Currently Owing: $900.00\n  No calendar currently set up\n------------------------------------------------------")

@patch("telebot.telebot")
def test_view_credit_no_records(mock_telebot, mocker):
    setUp()
    mc = mock_telebot.return_value
    mc.send_message.return_value = True
    mocker.patch.object(credit_view, "helper")
    credit_view.helper.read_credit_json.return_value = {}

    message = create_message("sample")
    message.chat.id = 12345
    credit_view.run(message, mc)
    assert mc.send_message.call_args_list[0] == call(12345, "You currently have no credit records.")

@patch("telebot.telebot")
def test_view_credit_no_user_records(mock_telebot, mocker):
    setUp()
    mc = mock_telebot.return_value
    mc.send_message.return_value = True
    mocker.patch.object(credit_view, "helper")
    credit_view.helper.read_credit_json.return_value = sample_data

    message = create_message("sample")
    message.chat.id = 12344
    credit_view.run(message, mc)
    assert mc.send_message.call_args_list[0] == call(12344, "You currently have no credit records.")

@patch("telebot.telebot")
def test_setup_credit(mock_telebot, mocker):
    setUp()
    mc = mock_telebot.return_value
    mc.send_message.return_value = True
    mocker.patch.object(credit_setup, "helper")
    credit_setup.helper.read_credit_json.return_value = sample_data

    message = create_message("sample")
    message.text = "account 2"
    message.chat.id = 12345
    credit_setup.handle_account_name(message, mc)
    assert mc.send_message.call_args_list[0] == call(12345, "What's the recurring due date for this account? Enter a number between 1-28")

@patch("telebot.telebot")
def test_setup_credit_duplicate(mock_telebot, mocker):
    setUp()
    mc = mock_telebot.return_value
    mc.send_message.return_value = True
    mocker.patch.object(credit_setup, "helper")
    credit_setup.helper.read_credit_json.return_value = sample_data

    message = create_message("sample")
    message.text = "account 1"
    message.chat.id = 12345
    credit_setup.handle_account_name(message, mc)
    assert mc.send_message.call_args_list[0] == call(12345, "That account name is already taken!")


@patch("telebot.telebot")
def test_setup_credit_with_date_upper(mock_telebot, mocker):
    setUp()
    mc = mock_telebot.return_value
    mc.send_message.return_value = True
    mocker.patch.object(credit_setup, "helper")
    mocker.patch.object(credit_setup, "account_names")
    credit_setup.helper.read_credit_json.return_value = sample_data
    credit_setup.account_names = {12345:"account 1"}
    message = create_message("sample")
    message.text = "28"
    message.chat.id = 12345
    credit_setup.handle_due_date(message, mc)
    assert mc.send_message.call_args_list[0] == call(12345, "Successfully created a credit account with the name account 1")


@patch("telebot.telebot")
def test_setup_credit_with_date_lower(mock_telebot, mocker):
    setUp()
    mc = mock_telebot.return_value
    mc.send_message.return_value = True
    mocker.patch.object(credit_setup, "helper")
    mocker.patch.object(credit_setup, "account_names")
    credit_setup.helper.read_credit_json.return_value = sample_data
    credit_setup.account_names = {12345:"account 1"}
    message = create_message("sample")
    message.text = "1"
    message.chat.id = 12345
    credit_setup.handle_due_date(message, mc)
    assert mc.send_message.call_args_list[0] == call(12345, "Successfully created a credit account with the name account 1")


@patch("telebot.telebot")
def test_setup_credit_with_date_invalid(mock_telebot, mocker):
    setUp()
    mc = mock_telebot.return_value
    mc.send_message.return_value = True
    mocker.patch.object(credit_setup, "helper")
    credit_setup.helper.read_credit_json.return_value = sample_data
    credit_setup.account_names = {12345:"account 1"}
    message = create_message("sample")
    message.text = "29"
    message.chat.id = 12345
    credit_setup.handle_due_date(message, mc)
    assert mc.send_message.call_args_list[0] == call(12345, "Invalid due date, try again!")

@patch("telebot.telebot")
def test_delete(mock_telebot, mocker):
    setUp()
    mc = mock_telebot.return_value
    mc.send_message.return_value = True
    mocker.patch.object(credit_delete, "helper")
    credit_delete.helper.read_credit_json.return_value = sample_data
    message = create_message("sample")
    message.text = "account 1"
    message.chat.id = 12345
    credit_delete.handle_account_name(message, mc)
    assert mc.send_message.call_args_list[0] == call(12345, "account 1 was deleted!")

@patch("telebot.telebot")
def test_delete_invalid_name(mock_telebot, mocker):
    setUp()
    mc = mock_telebot.return_value
    mc.send_message.return_value = True
    mocker.patch.object(credit_delete, "helper")
    credit_delete.helper.read_credit_json.return_value = sample_data
    message = create_message("sample")
    message.text = "account 3"
    message.chat.id = 12345
    credit_delete.handle_account_name(message, mc)
    assert mc.send_message.call_args_list[0] == call(12345, "That account name doesn't exist!")

@patch("telebot.telebot")
def test_delete_invalid_no_accounts(mock_telebot, mocker):
    setUp()
    mc = mock_telebot.return_value
    mc.send_message.return_value = True
    mocker.patch.object(credit_delete, "helper")
    credit_delete.helper.read_credit_json.return_value = sample_data
    message = create_message("sample")
    message.text = "account 2"
    message.chat.id = 12344
    credit_delete.handle_account_name(message, mc)
    assert mc.send_message.call_args_list[0] == call(12344, "You do not have any credit accounts!")

@patch("telebot.telebot")
def test_delete_invalid_no_accounts_on_run(mock_telebot, mocker):
    setUp()
    mc = mock_telebot.return_value
    mc.send_message.return_value = True
    mocker.patch.object(credit_delete, "helper")
    credit_delete.helper.read_credit_json.return_value = sample_data
    message = create_message("sample")
    message.text = "account 2"
    message.chat.id = 12344
    credit_delete.run(message, mc)
    assert mc.send_message.call_args_list[0] == call(12344, "You do not have any credit accounts!")

@patch("telebot.telebot")
def test_pay_credit(mock_telebot, mocker):
    setUp()
    mc = mock_telebot.return_value
    mc.send_message.return_value = True
    mocker.patch.object(credit_pay, "helper")
    credit_pay.helper.read_credit_json.return_value = sample_data
    credit_pay.account_names = {12345:"account 1"}
    message = create_message("sample")
    message.text = "20"
    message.chat.id = 12345
    credit_pay.handle_payment(message, mc)
    assert mc.send_message.call_args_list[0] == call(12345, "You now owe $880.00")

@patch("telebot.telebot")
def test_clear_credit(mock_telebot, mocker):
    setUp()
    mc = mock_telebot.return_value
    mc.send_message.return_value = True
    mocker.patch.object(credit_clear, "helper")
    credit_clear.helper.read_credit_json.return_value = sample_data
    message = create_message("sample")
    message.text = "account 1"
    message.chat.id = 12345
    credit_clear.handle_account_name(message, mc)
    assert mc.send_message.call_args_list[0] == call(12345, "Account expenses cleared!")

@patch("telebot.telebot")
def test_credit_calendar_no_account_name(mock_telebot, mocker):
    setUp()
    mc = mock_telebot.return_value
    mc.send_message.return_value = True
    mocker.patch.object(credit_calendar, "helper")
    credit_calendar.helper.read_credit_json.return_value = sample_data
    credit_calendar.helper.read_oauth_json.return_value = {}
    message = create_message("sample")
    message.text = "Done"
    message.chat.id = 12345
    credit_calendar.handle_oauth(message, mc)
    assert mc.send_message.call_args_list[0] == call(12345, "Sorry, something went wrong. Try again later!") 


@patch("telebot.telebot")
def test_credit_calendar_no_oauth(mock_telebot, mocker):
    setUp()
    mc = mock_telebot.return_value
    mc.send_message.return_value = True
    mocker.patch.object(credit_calendar, "helper")
    credit_calendar.helper.read_credit_json.return_value = sample_data
    credit_calendar.helper.read_oauth_json.return_value = {}
    credit_calendar.account_names = {12345:"account 1"}
    message = create_message("sample")
    message.text = "Done"
    message.chat.id = 12345
    credit_calendar.handle_oauth(message, mc)
    assert mc.send_message.call_args_list[0] == call(12345, "Your oauth2 token was not generated properly!") 


def create_message(text):
    params = {"messagebody": text}
    chat = types.User(11, False, "test")
    return types.Message(1, None, None, chat, "text", params, "")




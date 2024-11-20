"""
File: test_add.py
Author: Vyshnavi Adusumelli, Tejaswini Panati, Harshavardhan Bandaru
Date: October 01, 2023
Description: File contains Telegram bot message handlers and their associated functions.

Copyright (c) 2023

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS," WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import os
import json
from mock.mock import patch
from telebot import types
import add
from mock import ANY, call
from datetime import datetime


dateFormat = "%d-%b-%Y"
timeFormat = "%H:%M"
monthFormat = "%b-%Y"
date = datetime.today().date()

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
def test_run(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mc.send_message.return_value = True

    message = create_message("hello from test run!")
    add.run(message, mc)
    assert mc.send_message.called


@patch("telebot.telebot")
def test_post_category_selection_working(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mc.send_message.return_value = True

    message = create_message("hello from testing!")
    add.post_category_selection(message, mc, date)
    assert mc.send_message.called


@patch("telebot.telebot")
def test_post_category_selection_noMatchingCategory(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mc.send_message.return_value = []
    mc.reply_to.return_value = True

    mocker.patch.object(add, "helper")
    add.helper.getSpendCategories.return_value = None

    message = create_message("hello from testing!")
    add.post_category_selection(message, mc, date)
    assert mc.reply_to.called


@patch("telebot.telebot")
def test_post_amount_input_working(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mc.send_message.return_value = True

    message = create_message("120")
    add.post_amount_input(message, mc, "Food", date)
    assert mc.send_message.called


@patch("telebot.telebot")
def test_add_expense_with_credit(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mc.send_message.return_value = True
    mocker.patch.object(add, "helper")
    add.helper.read_credit_json.return_value = sample_data

    message = create_message("sample")
    message.text = "Yes"
    message.chat.id = 12345
    add.credit_option(message, mc, "21-Aug-2024,Food,200.0")
    assert mc.send_message.called
    mc.send_message.assert_called_once_with(12345, "Which account do you want to add it to?", reply_markup=ANY)


@patch("telebot.telebot")
def test_add_expense_with_credit_no(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mc.send_message.return_value = True
    mocker.patch.object(add, "helper")
    add.helper.read_credit_json.return_value = sample_data

    message = create_message("sample")
    message.text = "No"
    message.chat.id = 12345
    add.credit_option(message, mc, "21-Aug-2024,Food,200.0")
    assert mc.send_message.called
    mc.send_message.assert_called_once_with(12345, "Alright, thank you!")


@patch("telebot.telebot")
def test_add_expense_with_credit_random_input(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mc.send_message.return_value = True
    mocker.patch.object(add, "helper")
    add.helper.read_credit_json.return_value = sample_data

    message = create_message("sample")
    message.text = "ooga booga"
    message.chat.id = 12345
    add.credit_option(message, mc, "21-Aug-2024,Food,200.0")
    assert mc.send_message.called
    mc.send_message.assert_called_once_with(12345, "Do you want to add this expense to your credit account for tracking?", reply_markup=ANY)


@patch("telebot.telebot")
def test_add_expense_with_credit_name(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mc.send_message.return_value = True
    mocker.patch.object(add, "helper")
    add.helper.read_credit_json.return_value = sample_data

    message = create_message("sample")
    message.text = "account 1"
    message.chat.id = 12345
    add.credit_name_input(message, mc, "21-Aug-2024,Food,200.0")
    assert mc.send_message.call_args_list[1] == call(12345, "What you owe for the account now 900.0 --> 1100.0")


@patch("telebot.telebot")
def test_add_expense_with_credit_name_invalid_name(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mc.send_message.return_value = True
    mocker.patch.object(add, "helper")
    add.helper.read_credit_json.return_value = sample_data

    message = create_message("sample")
    message.text = "account"
    message.chat.id = 12345
    add.credit_name_input(message, mc, "21-Aug-2024,Food,200.0")
    assert mc.send_message.call_args_list[0] == call(12345, "That account name doesn't exist!")

@patch("telebot.telebot")
def test_add_expense_with_credit_name_invalid_number(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mc.send_message.return_value = True
    mocker.patch.object(add, "helper")
    add.helper.read_credit_json.return_value = sample_data

    message = create_message("sample")
    message.text = "account 1"
    message.chat.id = 12345
    add.credit_name_input(message, mc, "21-Aug-2024,Food,ooga")
    assert mc.send_message.call_args_list[1] == call(12345, "Please enter a valid number for the expense.")


@patch("telebot.telebot")
def test_post_amount_input_working_withdata(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mc.send_message.return_value = True
    mocker.patch.object(add, "helper")
    add.helper.validate_entered_amount.return_value = 10
    add.helper.write_json.return_value = True
    add.helper.getDateFormat.return_value = dateFormat
    add.helper.getTimeFormat.return_value = timeFormat

    mocker.patch.object(add, "option")
    add.option.return_value = {11, "here"}

    message = create_message("hello from testing!")
    add.post_amount_input(message, mc, "Food", date)
    assert mc.send_message.called


@patch("telebot.telebot")
def test_post_amount_input_nonworking(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mc.send_message.return_value = True
    mc.reply_to.return_value = True
    mocker.patch.object(add, "helper")
    add.helper.validate_entered_amount.return_value = 0
    message = create_message("hello from testing!")
    add.post_amount_input(message, mc, "Food",date)
    assert mc.send_message.called


@patch("telebot.telebot")
def test_post_amount_input_working_withdata_chatid(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mc.send_message.return_value = True
    mocker.patch.object(add, "helper")
    add.helper.validate_entered_amount.return_value = 10
    add.helper.write_json.return_value = True
    add.helper.getDateFormat.return_value = dateFormat
    add.helper.getTimeFormat.return_value = timeFormat

    mocker.patch.object(add, "option")
    add.option = {11, "here"}
    test_option = {}
    test_option[11] = "here"
    add.option = test_option

    message = create_message("hello from testing!")
    add.post_amount_input(message, mc, "Food", date)
    assert mc.send_message.called
    # assert mc.send_message.called_with(11, ANY)


def test_add_user_record_nonworking(mocker):
    mocker.patch.object(add, "helper")
    add.helper.read_json.return_value = {}
    addeduserrecord = add.add_user_record(1, "record : test")
    assert addeduserrecord


def test_add_user_record_working(mocker):
    MOCK_USER_DATA = test_read_json()
    mocker.patch.object(add, "helper")
    add.helper.read_json.return_value = MOCK_USER_DATA
    addeduserrecord = add.add_user_record(1, "record : test")
    if len(MOCK_USER_DATA) + 1 == len(addeduserrecord):
        assert True


def create_message(text):
    params = {"messagebody": text}
    chat = types.User(11, False, "test")
    return types.Message(1, None, None, chat, "text", params, "")


def test_read_json():
    try:
        if not os.path.exists("./test/dummy_expense_record.json"):
            with open("./test/dummy_expense_record.json", "w") as json_file:
                json_file.write("{}")
            return json.dumps("{}")
        elif os.stat("./test/dummy_expense_record.json").st_size != 0:
            with open("./test/dummy_expense_record.json") as expense_record:
                expense_record_data = json.load(expense_record)
            return expense_record_data

    except FileNotFoundError:
        print("---------NO RECORDS FOUND---------")
"""
File: helper.py
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

import re
import json
import os
import csv
import yfinance as yf
from datetime import datetime
from tabulate import tabulate

spend_categories = []
choices = ["Date", "Category", "Cost"]
spend_display_option = ["Day", "Month"]
spend_estimate_option = ["Next day", "Next month"]
update_options = {"continue": "Continue", "exit": "Exit"}
budget_options = {"update": "Add/Update", "view": "View", "delete": "Delete"}
budget_types = {"overall": "Overall Budget",
                "category": "Category-Wise Budget"}
data_format = {"data": [], "budget": {
    "overall": "0", "category": None}, "groupdata": []}
analytics_options = {"overall": "Overall budget split by Category", "spend": "Split of current month expenditure",
                     "remaining": "Remaining value", "history": "Time series graph of spend history"}
portfolio_options = {"buy": "Buy a Stock",
                     "sell": "Sell a Stock", "view": "View Portfolio"}
portfolio_format = {"stocks": []}

# set of implemented commands and their description
commands = {
    "menu": "Display commands with their descriptions.",
    "help": "Display the list of commands.",
    "pdf": "Provides expense history as PDF. It contains the following expense charts - \
       \n 1. Budget split - total budget and budget for various categories as a pie chart \
       \n 2. Category wise spend split - Distribution of expenses for each category as a pie chart \
       \n 3. Category wise budget command - Split of used and remaining percentage of the budget amount for every category  \
       \n 4. Time series of the expense - Time Vs Expense in $",
    "add": "This option is for adding your expenses \
       \n 1. It will give you the list of categories to choose from. \
       \n 2. You will be prompted to enter the amount corresponding to your spending \
       \n 3. The message will be prompted to notify the addition of your expense with the amount,date, time and category \
       \n 4. The message will ask if you would like to add your expense to your credit account to track what you owe \
       \n 5. You will be prompted to add in the name of your account, please create this with /setup_credit",
    "add_recurring": "This option is to add a recurring expense for future months",
    "analytics": "This option gives user a graphical representation of their expenditures \
        \n You will get an option to choose the type of data you want to see.",
    "predict": "This option analyzes your recorded spendings and gives you a budget that will accommodate for them.",
    "history": "This option is to give you the detailed summary of your expenditure with Date, time ,category and amount. A quick lookup into your spending. You can view in different currency",
    "delete": "This option is to Clear/Erase specific records or all your records based on your Choice",
    "display": "This option is to display your records for the current month or for the current day as per the user's choice.",
    "edit": "This option helps you to go back and correct/update the missing details \
        \n 1. It will give you the list of your expenses you wish to edit \
        \n 2. It will let you change the specific field based on your requirements like amount/date/category",
    "budget": "This option is to set/update/delete the budget. \
        \n 1. The Add/update category is to set the new budget or update the existing budget \
        \n 2. The view category gives the detail if budget is exceeding or in limit with the difference amount \
        \n 3. The delete category allows to delete the budget and start afresh!  ",
    "updateCategory": "This option is to add/delete/edit the categories. \
        \n 1. The Add Category option is to add a new category which dosen't already exist \
        \n 2. The Delete Category option is to delete an existing category \
        \n 3. The Edit Category option is to edit an existing category. ",
    "weekly": "This option is to get the weekly analysis report of the expenditure",
    "monthly": "This option is to get the monthly analysis report of the expenditure",
    "sendEmail": "Send an email with an attachment showing your history",
    "group": "This option is to manage groups. To create, delete and view groups",
    "chat": "Start a conversation with ChatGPT",
    "currency": "Lists all supported currencies, allowing users to view available options for conversions.",
    "convert": "Converts a specified currency to USD and provides the current exchange rate.",
    "currencycalculator": "Guides users through a step-by-step currency conversion process, allowing selection of base and target currencies.",
    "portfolio": "Buy/sell stock and view your portfolio.",
    "historicaltrends": "Guides users to select two types of currency and shows a comparative historical trend between the two",
    "view_credit": "Lists the credit accounts the user has with corresponding expenses and due dates.",
    "setup_credit": "Sets up a credit account for the user.",
    "pay_credit": "Pays off certain amount of the credit account the user has. Can be used to adjust what you owe for discrepancies.",
    "clear_credit": "Remove the expenses for an account",
    "delete_credit": "Remove a credit account",
    "setup_credit_calendar": "Add a credit account due date onto your google calendar and make it recurring"

}

dateFormat = "%d-%b-%Y"
timeFormat = "%H:%M"
monthFormat = "%b-%Y"

# === Documentation of helper.py ===

# function to load .json expense record data


def read_json():
    """
    read_json(): Function to load .json expense record data
    """
    try:
        if not os.path.exists("expense_record.json") or os.stat("expense_record.json").st_size == 0:
            with open("expense_record.json", "w", encoding="utf-8") as json_file:
                json_file.write("{}")
            return json.dumps("{}")
        elif os.stat("expense_record.json").st_size != 0:
            with open("expense_record.json", encoding="utf-8") as expense_record:
                expense_record_data = json.load(expense_record)
            return expense_record_data

    except FileNotFoundError:
        print("---------NO RECORDS FOUND---------")


def write_json(user_list):
    """
    write_json(user_list): Stores data into the datastore of the bot.
    """
    try:
        with open("expense_record.json", "w", encoding="utf-8") as json_file:
            json.dump(user_list, json_file, ensure_ascii=False, indent=4)
    except FileNotFoundError:
        print("Sorry, the data file could not be found.")


def read_category_json():
    """
    read_category_json(): Function to load .json category data
    """
    try:
        if not os.path.exists("categories.json"):
            with open("categories.json", "w", encoding="utf-8") as json_file:
                json_file.write(
                    "{ \"categories\" : \"Food,Groceries,Utilities,Transport,Shopping,Miscellaneous\" }")
            return json.dumps("{ \"categories\" : \"\" }")
        elif os.stat("categories.json").st_size != 0:
            with open("categories.json", encoding="utf-8") as category_record:
                category_record_data = json.load(category_record)
            return category_record_data

    except FileNotFoundError:
        print("---------NO CATEGORIES FOUND---------")


def write_category_json(category_list):
    """
    write_category_json(category_list): Stores data into the datastore of the bot.
    """
    try:
        with open("categories.json", "w", encoding="utf-8") as json_file:
            json.dump(category_list, json_file, ensure_ascii=False, indent=4)
    except FileNotFoundError:
        print("Sorry, the data file could not be found.")


def read_portfolio_json():
    """
    read_json(): Function to load .json portfolio data
    """
    try:
        if not os.path.exists("portfolio.json") or os.stat("portfolio.json").st_size == 0:
            with open("portfolio.json", "w", encoding="utf-8") as json_file:
                json_file.write("{}")
            return json.dumps("{}")
        elif os.stat("portfolio.json").st_size != 0:
            with open("portfolio.json", encoding="utf-8") as portfolio:
                portfolio_data = json.load(portfolio)
            return portfolio_data

    except FileNotFoundError:
        print("---------NO PORTFOLIO FOUND---------")


def write_portfolio_json(user_list):
    """
    write_json(user_list): Stores data into the datastore of the bot.
    """
    try:
        with open("portfolio.json", "w", encoding="utf-8") as json_file:
            json.dump(user_list, json_file, ensure_ascii=False, indent=4)
    except FileNotFoundError:
        print("Sorry, the data file could not be found.")


def read_credit_json():
    """
    read_credit_json(): Function to load .json credit record data
    """
    try:
        if not os.path.exists("credit_record.json"):
            with open("credit_record.json", "w+", encoding="utf-8") as json_file:
                json_file.write("{}")
            return {}
        elif os.stat("credit_record.json").st_size != 0:
            with open("credit_record.json", encoding="utf-8") as credit_record:
                credit_record_data = json.load(credit_record)
                return credit_record_data
            return credit_record_data

    except FileNotFoundError:
        print("---------NO CREDIT RECORDS FOUND---------")


def write_credit_json(credit_list):
    """
    write_credit_json(credit_list): Stores credit data into the datastore of the bot.
    """
    try:
        with open("credit_record.json", "w+", encoding="utf-8") as json_file:
            json.dump(credit_list, json_file, ensure_ascii=False, indent=4)
    except FileNotFoundError:
        print("Sorry, the data file could not be found.")


def read_oauth_json():
    """
    read_oauth_json(): Function to load .json oauth record data
    """
    try:
        if not os.path.exists("oauth_record.json"):
            with open("oauth_record.json", "w+", encoding="utf-8") as json_file:
                json_file.write("{}")
            return {}
        elif os.stat("oauth_record.json").st_size != 0:
            with open("oauth_record.json", encoding="utf-8") as oauth_record:
                oauth_record_data = json.load(oauth_record)
                return oauth_record_data if oauth_record_data else {}
            return oauth_record_data

    except FileNotFoundError:
        print("---------NO OAUTH RECORDS FOUND---------")


def write_oauth_json(oauth_record):
    """
    write_oauth_json(oauth_record): Stores credit data into the datastore of the bot.
    """
    try:
        with open("oauth_record.json", "w+", encoding="utf-8") as json_file:
            json.dump(oauth_record, json_file, ensure_ascii=False, indent=4)
    except FileNotFoundError:
        print("Sorry, the data file could not be found.")


def validate_entered_amount(amount_entered):
    """
    validate_entered_amount(amount_entered): Takes 1 argument, amount_entered.
    It validates this amount's format to see if it has been correctly entered by the user.
    """
    if amount_entered is None:
        return 0
    if re.match("^[1-9][0-9]{0,14}\\.[0-9]*$", amount_entered) or re.match(
        "^[1-9][0-9]{0,14}$", amount_entered
    ):
        amount = round(float(amount_entered), 2)
        if amount > 0:
            return str(amount)
    return 0


def validate_entered_duration(duration_entered):
    """
    Validates the entered duration from the user to see if its valid
    """
    if duration_entered is None:
        return 0
    if re.match("^[1-9][0-9]{0,14}", duration_entered):
        duration = int(duration_entered)
        if duration > 0:
            return str(duration)
    return 0


def getPortfolioData(chat_id):
    """
    Returns a string output of the user's portfolio
    """
    user_list = read_portfolio_json()
    if user_list is None:
        return ""
    elif user_list.get(str(chat_id), None) is None:
        return ""
    elif not user_list[str(chat_id)]["stocks"]:
        return ""
    else:
        portfolio = user_list[str(chat_id)]["stocks"]
        table = [["Stock", "Shares", "Buy Price",
                  "Current Price", "Percent Change"]]
        portfolio_csv = csv.reader(portfolio)
        portfolio_worth = 0
        for stock in portfolio_csv:
            ticker = yf.Ticker(stock[0])
            curr_price = ticker.info['currentPrice']
            curr_price = round(curr_price, 2)
            percent_change = ((curr_price / float(stock[2])) - 1.0) * 100
            percent_change = round(percent_change, 2)
            portfolio_worth += int(stock[1]) * curr_price
            table.append([stock[0], stock[1], "$ " + stock[2],
                          "$ " + str(curr_price), str(percent_change) + "%"])
        output = "Your portfolio is worth ${:.2f}".format(portfolio_worth)
        portfolio_table = "<pre>" + \
            tabulate(table, headers='firstrow')+"</pre>"
        output += "\n" + portfolio_table
        return output


def getUserHistory(chat_id):
    """
    getUserHistory(chat_id): Takes 1 argument chat_id and uses this to get the relevant user's historical data.
    """
    data = getUserData(chat_id)

    if data is not None:
        return_data = []
        return_data += data["data"]
        group_data = data.get("groupdata", [])
        if group_data:
            temp = []
            for gd in group_data:
                cols = gd.split(",")
                temp_str = str(cols[0]) + "," + \
                    str(cols[1]) + "," + str(cols[2])
                temp.append(temp_str)
            group_data = temp
        return_data += group_data
        return return_data
    return None


def getUserHistoryByCategory(chat_id, category):
    """
    Takes 2 arguments chat_id and category and returns 
    the expenses from a specific category for a given chat id.
    """
    data = getUserHistory(chat_id)
    previous_expenses = []
    for record in data:
        if f",{category}," in record:
            previous_expenses.append(record)
    return previous_expenses


def getUserHistoryByDate(chat_id, date):
    """
    Returns the expenses from a specific date for a given chat id
    """
    data = getUserHistory(chat_id)
    previous_expenses = []
    for record in data:
        if f"{date}," in record:
            previous_expenses.append(record)
    return previous_expenses


def getUserHistoryDateExpense(chat_id):
    """
    Returns the expenses for a user
    """
    data = getUserHistory(chat_id)
    cat_spend_dict = {}
    for record in data:
        split_vals = record.split(",")
        cat_spend_dict[split_vals[0]] = split_vals[2]
    return cat_spend_dict


def getUserData(chat_id):
    """
    This function gives all the data related to a 
    user from the chat_id. Includes budgets and expenses.
    """
    user_list = read_json()
    if user_list is None:
        return None
    if str(chat_id) in user_list:
        return user_list[str(chat_id)]
    return None


def throw_exception(e, message, bot, logging):
    """
    Used for error handling in bot code. Throws 
    exception if any is thrown by another part of code.
    """
    logging.exception(str(e))
    bot.reply_to(message, "Oh no! " + str(e))


def createNewUserRecord():
    """
    Creates a new record for a newly registered user
    """
    return data_format


def createNewPortfolioUserRecord():
    """
    Creates a new portfolio record for a newly registered user
    """
    return portfolio_format


def getOverallBudget(chatId):
    """
    Returns overall budget value for given user
    """
    data = getUserData(chatId)
    if data is None or data == {}:
        return None
    return data["budget"]["overall"]


def getCategoryBudget(chatId):
    """
    Returns category-wise budget split for given user
    """
    data = getUserData(chatId)
    if data is None:
        return None
    return data["budget"]["category"]


def getCategoryBudgetByCategory(chatId, cat):
    """
    Returns specific category's budget allocation
    """
    if not isCategoryBudgetByCategoryAvailable(chatId, cat):
        return None
    data = getCategoryBudget(chatId)
    return data[cat]


def canAddBudget(chatId):
    """
    Returns whether a user can add to their budget
    """
    overall_budget = getOverallBudget(chatId)
    category_budget = getCategoryBudget(chatId)
    return (overall_budget is None and overall_budget != '0') and (category_budget is None and category_budget != {})


def isOverallBudgetAvailable(chatId):
    """
    Checks whether overall budget is initialized or not
    """
    overall_budget = getOverallBudget(chatId)
    if overall_budget is not None and overall_budget != '0':
        return True
    return False


def isCategoryBudgetAvailable(chatId):
    """
    Checks whether category wise budget is initialized or not
    """
    category_budget = getCategoryBudget(chatId)
    if category_budget is not None and category_budget != {}:
        return True
    return False


def isCategoryBudgetByCategoryAvailable(chatId, cat):
    """
    Checks whether specified category's budget is initialized or not
    """
    data = getCategoryBudget(chatId)
    if data is None or data == {} or data == '0':
        return False
    return cat in data.keys()


def isCategoryBudgetByCategoryNotZero(chatId):
    """
    Checks whether the budget for categories is non-zero
    """
    for cat in spend_categories:
        if getCategoryBudgetByCategory(chatId, cat) == '0':
            return False
    return True


def get_uncategorized_amount(chatId, amount):
    """
    Calculates the portion of the budget that is not assigned to any specific category
    """
    overall_budget = float(amount)
    category_budget_data = getCategoryBudget(chatId)
    if category_budget_data is None or category_budget_data == {}:
        return amount
    category_budget = 0
    for c in category_budget_data.values():
        category_budget += float(c)
    uncategorized_budget = overall_budget - category_budget
    return str(round(uncategorized_budget, 2))


def display_remaining_budget(message, bot):
    """
    Displays remaining budget
    """
    display_remaining_overall_budget(message, bot)


def display_remaining_overall_budget(message, bot):
    """
    Displays overall budget after recorded expenses
    """
    chat_id = message.chat.id
    remaining_budget = calculateRemainingOverallBudget(chat_id)
    if remaining_budget >= 0:
        msg = "\nRemaining Overall Budget is $" + str(remaining_budget)
    else:
        msg = (
            "\nBudget Exceded!\nExpenditure exceeds the budget by $" +
            str(remaining_budget)[1:]
        )
    bot.send_message(chat_id, msg)


def calculateRemainingOverallBudget(chat_id):
    """
    Calculate remaining overall budget after recorded expenses
    """
    budget = getOverallBudget(chat_id)
    history = getUserHistory(chat_id)
    query = datetime.now().today().strftime(getMonthFormat())
    queryResult = [value for _, value in enumerate(
        history) if str(query) in value]
    if budget == None:
        return -calculate_total_spendings(queryResult)
    return float(budget) - calculate_total_spendings(queryResult)


def calculate_total_spendings(queryResult):
    """
    Calculate total spendings of the user
    """
    total = 0
    for row in queryResult:
        s = row.split(",")
        total = total + float(s[2])
    return total


def calculateRemainingCategoryBudget(chat_id, cat):
    """
    Calculate remaining category budget after recorded expenses in the specific category
    """
    budget = getCategoryBudgetByCategory(chat_id, cat)
    history = getUserHistory(chat_id)
    query = datetime.now().today().strftime(getMonthFormat())
    queryResult = [value for _, value in enumerate(
        history) if str(query) in value]
    return float(budget) - calculate_total_spendings_for_category(queryResult, cat)


def calculateRemainingCategoryBudgetPercent(chat_id, cat):
    """
    Calculate percentage of spent money on a particular category against its budget.
    """
    budget = getCategoryBudgetByCategory(chat_id, cat)
    history = getUserHistory(chat_id)
    query = datetime.now().today().strftime(getMonthFormat())
    queryResult = [value for _, value in enumerate(
        history) if str(query) in value]
    if budget == '0':
        print("budget is zero")
        return None
    return (calculate_total_spendings_for_category(queryResult, cat)/float(budget))*100


def calculate_total_spendings_for_category(queryResult, cat):
    """
    Calculate total spending of the user within a specific category
    """
    total = 0
    for row in queryResult:
        s = row.split(",")
        if cat == s[1]:
            total = total + float(s[2])
    return total


def calculate_total_spendings_for_category_chat_id(chat_id, cat):
    """
    Calculate total spending of the user within a specific category
    """
    history = getUserHistory(chat_id)
    query = datetime.now().today().strftime(getMonthFormat())
    queryResult = [value for _, value in enumerate(
        history) if str(query) in value]
    return calculate_total_spendings_for_category(queryResult, cat)


def updateBudgetCategory(chatId, category):
    """
    Initializes the specific budget category
    """
    user_list = read_json()
    user_list[str(chatId)]["budget"]["category"][category] = str(0)
    write_json(user_list)


def deleteBudgetCategory(chatId, category):
    """
    Deletes the specified budget category
    """
    user_list = read_json()
    user_list[str(chatId)]["budget"]["category"].pop(category, None)
    write_json(user_list)


def getAvailableCategories(history):
    """
    Get available categories from history data
    """
    available_categories = set()
    for record in history:
        available_categories.add(record.split(',')[1])
    return available_categories


def getCategoryWiseSpendings(available_categories, history):
    """
    Get category wise spending details
    """
    category_wise_history = {}
    for cat in available_categories:
        for record in history:
            if cat in record:
                if cat in category_wise_history.keys():
                    category_wise_history[cat].append(record)
                else:
                    category_wise_history[cat] = [record]
    return category_wise_history


def getFormattedPredictions(category_predictions):
    """
    Format predictions into readable format from dictionary into 
    string in order to send message to the user.
    """
    category_budgets = ""
    for key, value in category_predictions.items():
        if type(value) == float:
            category_budgets += str(key) + ": $" + str(value) + "\n"
        else:
            category_budgets += str(key) + ": " + value + "\n"
    predicted_budget = "Here are your predicted budgets"
    predicted_budget += " for the next month \n"
    predicted_budget += category_budgets
    return predicted_budget


def getSpendCategories():
    """
    getSpendCategories(): This functions returns the spend categories used in the bot. These are defined the same file.
    """
    category_list = read_category_json()
    if category_list is None:
        return None
    spend_cat = category_list["categories"].split(',')
    spend_cat = [category.strip()
                 for category in spend_cat if category.strip()]

    return spend_cat


def deleteSpendCategories(category):
    """
    Deletes the spending category
    """
    category_list = read_category_json()
    if category_list is None:
        return None
    spend_cat = category_list["categories"].split(',')
    spend_cat.remove(category)

    result = ','.join(spend_cat)
    category_list["categories"] = result
    write_category_json(category_list)


def addSpendCategories(category):
    """
    Adds a spending category
    """
    category_list = read_category_json()
    if category_list is None:
        return None
    spend_cat = category_list["categories"].split(',')
    spend_cat.append(category)
    spend_cat = [category.strip()
                 for category in spend_cat if category.strip()]
    result = ','.join(spend_cat)
    category_list["categories"] = result
    write_category_json(category_list)


def getSpendDisplayOptions():
    """
    getSpendDisplayOptions(): This functions returns the spend display options used in the bot. These are defined the same file.
    """
    return spend_display_option


def getSpendEstimateOptions():
    """
    Gets spend estimate options
    """
    return spend_estimate_option


def getCommands():
    """
    getCommands(): This functions returns the command options used in the bot. These are defined the same file.
    """
    return commands


def getDateFormat():
    """
    getCommands(): This functions returns the command options used in the bot. These are defined the same file.
    """
    return dateFormat


def getTimeFormat():
    """
    def getTimeFormat(): This functions returns the time format used in the bot.
    """
    return timeFormat


def getMonthFormat():
    """
    def getMonthFormat(): This functions returns the month format used in the bot.
    """
    return monthFormat


def getChoices():
    """
    Gets choices
    """
    return choices


def getBudgetOptions():
    """
    This function returns the budget options used by the bot. 
    These are defined in the same file.
    """
    return budget_options


def getBudgetTypes():
    """
    This function returns the types of budgets that can be set up by users. 
    These are defined in the same file.
    """
    return budget_types


def getUpdateOptions():
    """
    This function returns the update options used by the bot. 
    These are defined in the same file.
    """
    return update_options


def getAnalyticsOptions():
    """
    This function returns the analytics options used by the bot. 
    These are defined in the same file.
    """
    return analytics_options


def getPortfolioOptions():
    """
    This function returns the options for working with your portfolio.
    """
    return portfolio_options


def save_group_data(groups):
    """
    Saves group data
    """
    with open("groups.json", "w") as file:
        json.dump(groups, file, indent=4)


def load_group_data():
    """
    Loads group data
    """
    try:
        with open("groups.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

"""
File: currency.py
Author: Jiewen Liu
Date: October, 2024
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

import requests
import datetime
from pandas_datareader import data

API_URL = "https://v6.exchangerate-api.com/v6"
API_KEY = "6b3e6f09c28d0a24ba44ac29"

"""
Exchange codes for historical data from: 
https://fred.stlouisfed.org/categories/95
Here we are looking for currencies they provide
that convert into USD
"""
HISTORICAL_EXCHANGE_CODES = {
    "JPY": "EXJPUS",
    "CNY": "EXCHUS",
    "CAD": "EXCAUS",
    "KRW": "EXKOUS",
    "MXN": "EXMXUS",
    "INR": "EXINUS",
    "HKD": "EXHKUS"
}

def get_supported_currencies():
    """
    Fetches all the supported currencies from ExchangeRate-API.

    :return: A list of supported currency codes or None if the API call fails.
    """
    try:
        response = requests.get(f"{API_URL}/{API_KEY}/codes")
        if response.status_code == 200:
            data = response.json()
            if data['result'] == 'success':
                return [code[0] for code in data['supported_codes']]
            else:
                print("API error: ", data.get('error-type', 'Unknown error'))
        else:
            print(f"HTTP error: Status code {response.status_code}")
    except Exception as e:
        print(f"Error fetching supported currencies: {e}")
    return None

def get_supported_historical_currencies():
    """
    Returns the list of currencies supported for historical trends
    """
    return HISTORICAL_EXCHANGE_CODES.keys()

def get_conversion_rate(base_currency, target_currency):
    """
    Fetches the conversion rate from base_currency to target_currency.

    :param base_currency: The currency code you want to convert from (e.g., 'USD')
    :param target_currency: The currency code you want to convert to (e.g., 'EUR')
    :return: The conversion rate or None if the API call fails
    """
    try:
        response = requests.get(f"{API_URL}/{API_KEY}/latest/{base_currency}")
        if response.status_code == 200:
            data = response.json()
            if data['result'] == 'success':
                return data['conversion_rates'].get(target_currency)
            else:
                print("API error: ", data.get('error-type', 'Unknown error'))
        else:
            print(f"HTTP error: Status code {response.status_code}")
    except Exception as e:
        print(f"Error fetching conversion rate: {e}")
    return None

def get_historical_trend(base_currency, years=5, test_end=None):
    """
    Fetches the historical data from a specific currency types
    conversion rate compared to the USD

    :param base_currency: The currency code you want to get data
    :return: List of values over the past 10 years
    """
    if not base_currency in HISTORICAL_EXCHANGE_CODES.keys():
        return None
    
    if type(years) is not int:
        return None
    
    if years < 1:
        return None
    
    if years > 10:
        return None

    if not test_end:
        today = datetime.date.today()
        end = datetime.date(today.year, today.month, 1)
    else:
        end = test_end
    start = datetime.date(end.year - years, end.month, 1)

    try:
       historical_data = data.DataReader(HISTORICAL_EXCHANGE_CODES[base_currency], 'fred', start=start, end=end)

       return historical_data
    except Exception as e:
        print(f"Error fetcching historical data: {e}")

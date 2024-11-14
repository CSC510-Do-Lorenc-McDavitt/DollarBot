"""
File: portfolio.py
Author: Nathan Lorenc
Date: November 13, 2024
Description: File contains functionality for retrieving
stock portfolio prices for the user.
"""

import yfinance as yf
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

def buyStock(stock: str, numShares: int, pricePerShare: float):
    ticker = yf.Ticker(stock)
    print(ticker.history(period="1mo"))
    return 0

def sellStock(stock: str, numShares: int):
    return 0

def viewPortfolioTable():
    return 0

def viewPortfolioGraphWeek():
    # Tickers.download()
    return 0

def viewPortfolioGraphMonth():
    # Tickers.download()
    return 0

def viewPortfolioGraphYear():
    # Tickers.download()
    return 0

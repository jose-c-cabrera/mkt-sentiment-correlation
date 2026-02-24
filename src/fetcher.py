import yfinance as yf
import pandas as pd

class MarketDataFetcher:
    def __init__(self, ticker_symbol):
        self.ticker_symbol = ticker_symbol
        self.ticker = yf.Ticker(ticker_symbol)

    def get_headlines(self):
        news = self.ticker.news
        return news
    
    def get_stock_prices(self, period="1mo", interval="1d"):
        history = self.ticker.history(period=period, interval = interval)
        return history
    
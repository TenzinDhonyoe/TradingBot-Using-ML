from lumibot.brokers import Alpaca  # Import Alpaca broker
from lumibot.backtesting import YahooDataBacktesting  # Import Yahoo backtesting data
from lumibot.strategies.strategy import Strategy  # Import Strategy class
from lumibot.traders import Trader  # Import Trader class
from datetime import datetime  # Import datetime module
from alpaca_trade_api import REST  # Import Alpaca REST API
from timedelta import Timedelta  # Import Timedelta for date manipulation
from utils import estimate_sentiment  # Import sentiment estimation utility

API_KEY = ""  # Add Alpaca API key
API_SECRET = ""  # Add Alpaca API secret
BASE_URL = ""  # Add Alpaca base URL for paper trading

ALPACA_CREDS = {
    "API_KEY": API_KEY, 
    "API_SECRET": API_SECRET, 
    "PAPER": True  # Credentials dictionary for Alpaca
}

class MLTrader(Strategy): 
    def initialize(self, symbol: str = "SPY", cash_at_risk: float = .5): 
        self.symbol = symbol  # Trading symbol
        self.sleeptime = "24H"  # Sleep time between iterations
        self.last_trade = None  # Last trade action
        self.cash_at_risk = cash_at_risk  # Percentage of cash to risk
        self.api = REST(base_url=BASE_URL, key_id=API_KEY, secret_key=API_SECRET)  # Alpaca API initialization

    def position_sizing(self): 
        cash = self.get_cash()  # Get available cash
        last_price = self.get_last_price(self.symbol)  # Get last price of the symbol
        quantity = round(cash * self.cash_at_risk / last_price, 0)  # Calculate position size
        return cash, last_price, quantity

    def get_dates(self): 
        today = self.get_datetime()  # Get current date
        three_days_prior = today - Timedelta(days=3)  # Calculate date three days prior
        return today.strftime('%Y-%m-%d'), three_days_prior.strftime('%Y-%m-%d')

    def get_sentiment(self): 
        today, three_days_prior = self.get_dates()  # Get date range
        news = self.api.get_news(symbol=self.symbol, 
                                 start=three_days_prior, 
                                 end=today)  # Fetch news within date range
        news = [ev.__dict__["_raw"]["headline"] for ev in news]  # Extract headlines
        probability, sentiment = estimate_sentiment(news)  # Estimate sentiment
        return probability, sentiment 

    def on_trading_iteration(self): 
        cash, last_price, quantity = self.position_sizing()  # Determine position size
        probability, sentiment = self.get_sentiment()  # Get sentiment analysis

        #Only runs if I have cash available
        if cash > last_price: 
            if sentiment == "positive" and probability > .999: 
                if self.last_trade == "sell": 
                    self.sell_all()  # Sell existing positions
                order = self.create_order(
                    self.symbol, 
                    quantity, 
                    "buy", 
                    type="bracket", 
                    take_profit_price=last_price * 1.20, 
                    stop_loss_price=last_price * .95
                )
                self.submit_order(order)  # Submit buy order
                self.last_trade = "buy"
            elif sentiment == "negative" and probability > .999: 
                if self.last_trade == "buy": 
                    self.sell_all()  # Sell existing positions
                order = self.create_order(
                    self.symbol, 
                    quantity, 
                    "sell", 
                    type="bracket", 
                    take_profit_price=last_price * .8, 
                    stop_loss_price=last_price * 1.05
                )
                self.submit_order(order)  # Submit sell order
                self.last_trade = "sell"

start_date = datetime(2023, 1, 1)  # Backtest start date
end_date = datetime(2024, 6, 8)  # Backtest end date
broker = Alpaca(ALPACA_CREDS)  # Initialize Alpaca broker
strategy = MLTrader(name='mlstrat', broker=broker, 
                    parameters={"symbol": "SPY", 
                                "cash_at_risk": .5})  # Initialize strategy

strategy.backtest(
    YahooDataBacktesting, 
    start_date, 
    end_date, 
    parameters={"symbol": "SPY", "cash_at_risk": .5}  # Run backtest
)
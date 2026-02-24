from src.fetcher import MarketDataFetcher
from src.analyzer import SentimentAnalyzer
from src.utils import format_unix_timestamp, save_to_csv

def run_pipeline(ticker_symbol):
    # 1. Initialize
    fetcher = MarketDataFetcher(ticker_symbol)
    analyzer = SentimentAnalyzer()
    
    # 2. Extract News & Prices
    print(f"🚀 Starting pipeline for {ticker_symbol}...")
    raw_news = fetcher.get_headlines()
    # Fetching 1 month of historical price data
    df_prices = fetcher.get_stock_prices(period="1mo") 
    
    # 3. Transform News (Analyze & Format)
    df_sentiment = analyzer.process_headlines(raw_news)
    df_sentiment['date'] = df_sentiment['date'].apply(format_unix_timestamp)
    
    # 4. Load (Save both CSVs for the Dashboard)
    df_prices.reset_index(inplace=True) 
    
    save_to_csv(df_sentiment, f"{ticker_symbol}_sentiment.csv")
    save_to_csv(df_prices, f"{ticker_symbol}_prices.csv")
    
    print(f"✅ Success! Saved {len(df_sentiment)} headlines and {len(df_prices)} price points.")
    
    print("\n--- Sentiment Preview ---")
    print(df_sentiment[['date', 'mood', 'sentiment_score']].head())
    return df_sentiment, df_prices



if __name__ == "__main__":
    # Test it with a major stock
    target_stock = "TSLA" 
    run_pipeline(target_stock)
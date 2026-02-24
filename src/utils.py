import datetime
import pandas as pd

def format_unix_timestamp(timestamp):
    """Handles various timestamp formats to ensure we get a date."""
    if timestamp is None:
        return "N/A"
    try:
        # If it's already a datetime object or string, return as is
        if isinstance(timestamp, (int, float)):
            return datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M')
        return str(timestamp)
    except Exception:
        return "Format Error"
    
def calculate_rolling_sentiment(df, window=3):
    """
    Calculates a rolling average of sentiment to smooth out the noise.
    Great for showing 'Sentiment Momentum' on your dashboard.
    """
    if 'sentiment_score' in df.columns:
        # We ensure the data is sorted by date before rolling
        return df['sentiment_score'].rolling(window=window).mean()
    return None

def save_to_csv(df, filename):
    """Standardized way to save our data to the data/processed/ folder."""
    import os
    path = f"data/processed/{filename}"
    # Ensure directory exists
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_csv(path, index=False)
    print(f"Data saved to {path}")  
    
def get_correlation(df_sentiment, df_prices):
    # 1. Prepare Dates
    df_s = df_sentiment.copy()
    df_p = df_prices.copy()
    df_s['date_only'] = pd.to_datetime(df_s['date']).dt.date
    df_p['date_only'] = pd.to_datetime(df_p['Date']).dt.date

    # 2. Average sentiment per day
    daily_s = df_s.groupby('date_only')['sentiment_score'].mean().reset_index()

    # 3. Merge
    merged = pd.merge(daily_s, df_p, on='date_only')

    # 4. Handle Small Data
    if len(merged) < 2 or daily_s['sentiment_score'].std() == 0:
        return 0.0 # Standard dev of 0 means no change in mood = 0 correlation

    return round(merged['sentiment_score'].corr(merged['Close']), 4)
from textblob import TextBlob
import pandas as pd

class SentimentAnalyzer:
    @staticmethod
    def calculate_sentiment(text):
        if not text or text == "No Title":
            return 0.0
        
        # Get the standard score
        analysis = TextBlob(str(text))
        score = analysis.sentiment.polarity
        
        # Add "Financial Weighting" (Bonus for your CV!)
        bullish_words = ['growth', 'surge', 'beat', 'dividend', 'buy', 'upgrade']
        bearish_words = ['drop', 'miss', 'cut', 'slump', 'sell', 'downgrade', 'inflation']
        
        text_lower = text.lower()
        for word in bullish_words:
            if word in text_lower: score += 0.1
        for word in bearish_words:
            if word in text_lower: score -= 0.1
            
        return round(max(min(score, 1.0), -1.0), 4) # Keep it between -1 and 1

    def process_headlines(self, raw_news):
        processed_data = []
        
        if not raw_news:
            return pd.DataFrame()

        for article in raw_news:
            # 1.Data is now inside 'content'
            content = article.get('content', {})
            
            # Extract Title 
            title = content.get('title', 'No Title')
            
            # Extract Date 
            timestamp = content.get('pubDate') or article.get('providerPublishTime')

            # --- SENTIMENT CALCULATION ---
            score = self.calculate_sentiment(title)
            
            processed_data.append({
                "date": timestamp,
                "headline": title,
                "sentiment_score": score,
                "mood": "Bullish" if score > 0.05 else "Bearish" if score < -0.05 else "Neutral"
            })
            
        return pd.DataFrame(processed_data)
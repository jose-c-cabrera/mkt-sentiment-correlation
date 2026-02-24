# 📈 Market Mood Tracker: Sentiment-Price Correlation
A professional data pipeline that analyzes real-time financial news sentiment and correlates it with stock price movements. This project explores how "unstructured" news data (headlines) impacts "structured" financial data (time-series prices).
---
## 🚀 Key Features
Automated Data Pipeline: Extracts live news and historical price data using the yfinance API.

Sentiment Analysis: Leverages TextBlob with a custom financial keyword-weighting engine to score headlines from Bullish (+1) to Bearish (-1).

Dynamic Dashboard: Interactive UI built with Streamlit and Plotly featuring dual-axis time-series visualization.

Statistical Analysis: Calculates the Pearson Correlation Coefficient to determine the strength of the relationship between news mood and market volatility.

---

## 🛠️ Tech Stack
Language: Python 3.9+

Libraries: Pandas, NumPy, yfinance, TextBlob, Plotly

Framework: Streamlit (Web UI)

Architecture: Modular design with separate modules for Fetching, Analysis, and Utilities.

---

## 📁 Project Structure
```Plaintext
mkt-mood-corr/
├── data/
│ └── processed/ # Stores generated CSV files
├── src/
│ ├── fetcher.py # API connection logic
│ ├── analyzer.py # NLP and sentiment scoring
│ └── utils.py # Date formatting & correlation math
├── main.py # Entry point to run the pipeline
└── dashboard.py # Streamlit UI

```
---

## ⚙️ Installation & Usage
Clone the repository:

```Bash
git clone https://github.com/yourusername/mkt-mood-corr.git
cd mkt-mood-corr
```

Setup Virtual Environment:

```Bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Run the Pipeline:

```Bash
python main.py
```

Launch the Dashboard:

```Bash
streamlit run dashboard.py
```

---

## 📊 Methodology & Challenges
API Adaptation: Handled recent (Feb 2026) structural changes in the Yahoo Finance API by implementing a robust nested-key extraction logic for headlines and timestamps.

Sentiment Tuning: Since standard NLP often treats financial facts as "Neutral," I implemented a custom weighting layer to detect high-impact financial keywords (e.g., "dividend," "surge," "slump").

Correlation Strategy: To account for the limited news window of free APIs, the system is designed to accumulate data over time to build a statistically significant longitudinal dataset.

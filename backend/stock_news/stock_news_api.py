from datetime import datetime, timedelta
from textblob import TextBlob
import finnhub
from pymongo import MongoClient
from env import env
from flask import Blueprint
from datetime import datetime
import os 

news_analysis_module = Blueprint(env.route_news_analysis, __name__)

@news_analysis_module.route(env.route_news_analysis, methods=['GET'])
def news_analysis()->str:
    print("news_analysis")
    # === Step 0: MongoDB Setup ===
    # Fetch Mongo URI from environment variable, fallback to localhost
    mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    # Create MongoDB client
    client = MongoClient(mongo_uri)

    db = client["stock_predict"]  # Replace with your DB name
    buy_signal_col = db["buy_signal_track"]
    sentiment_col = db["stock_news_sentimental"]

    # Get list of stock symbols from MongoDB
    stock_symbols = list(buy_signal_col.distinct("stock_title"))
 
    # Get tickers already processed
    existing_tickers = sentiment_col.distinct('stock_title')

    # Separate into "new" and "already processed"
    new_tickers = [t for t in stock_symbols if t not in existing_tickers]
    existing_tickers_in_list = [t for t in stock_symbols if t in existing_tickers]

    # Final ordered list: new ones first
    ordered_tickers = new_tickers + existing_tickers_in_list

    # # === Step 1: Setup Finnhub client ===
    api_key = env.FIN_KEY  # Replace with your API key
    finnhub_client = finnhub.Client(api_key=api_key)

    # === Step 2: Define date range (last 7 days) ===
    today = datetime.now().date()
    week_ago = today - timedelta(days=3)

    # # === Step 3: Fetch company news ===
    news_by_symbol = {}

    for symbol in ordered_tickers:
        try:
            news = finnhub_client.company_news(
                symbol, 
                _from=week_ago.isoformat(), 
                to=today.isoformat()
            )
            if not news:
                print(f"❌ No news found for {symbol}")
                continue
            news_by_symbol[symbol] = news
            print(f"✅ Pulled {len(news)} articles for {symbol}")
        except Exception as e:
            print(f"❌ Failed to fetch news for {symbol}: {e}")
    
    # # === Step 4: Concatenate news text per company ===
    company_texts = {
        symbol: " ".join(f"{item['headline']} {item['summary']}" for item in news)
        for symbol, news in news_by_symbol.items()
    }

    # # === Step 5: Sentiment analysis function ===
    def analyze_sentiment(text):
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        if polarity > 0:
            sentiment = "Positive"
        elif polarity < 0:
            sentiment = "Negative"
        else:
            sentiment = "Neutral"
        return polarity, sentiment

    # # === Step 6: Apply sentiment analysis and store in MongoDB ===
    # sentiment_col.delete_many({})  # Optional: Clear old data

    for symbol, text in company_texts.items():
        polarity, sentiment = analyze_sentiment(text)
        
        result_doc = {
            "stock_title": symbol,
            "date": today.isoformat(),
            "insert_date": datetime.now(),
            "polarity": polarity,
            "sentiment": sentiment,
            "news_count": len(news_by_symbol.get(symbol, [])),
            "text_excerpt": text[:300] + "..." if len(text) > 300 else text  # Optional preview
        }
        
        sentiment_col.replace_one(
        {"stock_title": symbol},
        result_doc,
        upsert=True
    )
        print(f"📥 Stored sentiment for {symbol}: {sentiment} (Polarity: {polarity:.2f})")
    return {"status": "success"}

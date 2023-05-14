import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

def get_top_trending_stocks():
    rapidapi_key = os.getenv('RAPIDAPI_KEY')
    url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/market/get-trending-tickers"
    headers = {
        "x-rapidapi-key": rapidapi_key,
        "x-rapidapi-host": "apidojo-yahoo-finance-v1.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = json.loads(response.text)
        top_stocks = data['finance']['result'][0]['quotes'][:5]
        return [stock['symbol'] for stock in top_stocks]
    else:
        print(f"Error fetching trending stocks: {response.status_code}")
        return []


def get_stock_info(symbol):
    rapidapi_key = os.getenv('RAPIDAPI_KEY')
    url = f"https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v2/get-summary?symbol={symbol}&region=US"
    headers = {
        "x-rapidapi-key": rapidapi_key,
        "x-rapidapi-host": "apidojo-yahoo-finance-v1.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = json.loads(response.text)
        return {
            "price": data["price"]["regularMarketPrice"]["raw"],
            "market_cap": data["summaryDetail"]["marketCap"]["raw"],
            "volume": data["summaryDetail"]["volume"]["raw"],
            "day_high": data["summaryDetail"]["dayHigh"]["raw"],
            "day_low": data["summaryDetail"]["dayLow"]["raw"],
        }
    else:
        print(f"Error fetching stock information: {response.status_code}")
        return None

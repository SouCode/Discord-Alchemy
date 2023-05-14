import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

def get_stock_news(performance_id):
    rapidapi_key = os.getenv('RAPIDAPI_KEY')
    url = "https://ms-finance.p.rapidapi.com/news/list"
    querystring = {"performanceId": performance_id}
    headers = {
        "X-RapidAPI-Key": rapidapi_key,
        "X-RapidAPI-Host": "ms-finance.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)

    if response.status_code == 200:
        data = json.loads(response.text)
        return data
    else:
        print(f"Error fetching stock news: {response.status_code}")
        return None

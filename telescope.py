import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

def get_options_data(symbol):
    rapidapi_key = os.getenv('RAPIDAPI_KEY')
    url = f"https://telescope-stocks-options-price-charts.p.rapidapi.com/options/{symbol}"
    headers = {
        "X-RapidAPI-Key": rapidapi_key,
        "X-RapidAPI-Host": "telescope-stocks-options-price-charts.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = json.loads(response.text)
        options_data = data["optionChain"]["result"][0]["options"][0]["calls"]
        return options_data
    else:
        print(f"Error fetching options data: {response.status_code}")
        return None

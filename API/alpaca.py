import os
import alpaca_trade_api as tradeapi
from dotenv import load_dotenv

load_dotenv()

# Set up the Alpaca API instance
api_key = os.getenv('ALPACA_API_KEY')
secret_key = os.getenv('ALPACA_SECRET_KEY')
base_url = os.getenv('ALPACA_BASE_URL')

api = tradeapi.REST(api_key, secret_key, base_url, api_version='v2')

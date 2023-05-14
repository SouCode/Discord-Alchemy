import os
import requests
from dotenv import load_dotenv

load_dotenv()

def get_company_news(company):
    try:
        # Get the API key from environment variables
        api_key = os.getenv('NEWS_API_KEY')
        
        # Define the endpoint URL
        url = f"https://newsapi.org/v2/everything?q={company}&apiKey={api_key}"

        # Send the GET request
        response = requests.get(url)
        
        # Check the response status code
        if response.status_code != 200:
            return None
        
        # Parse the JSON response
        news_data = response.json()
        
        return news_data['articles']
    
    except Exception as e:
        print(f"Error occurred: {e}")
        return None

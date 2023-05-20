import os
import giphy_client
from dotenv import load_dotenv
from giphy_client.rest import ApiException

load_dotenv()

api_instance = giphy_client.DefaultApi()
api_key = os.getenv('GIPHY_API_KEY')  # Giphy API Key

def get_random_anime_gif():
    try:
        # Get random gif from GIPHY API
        response = api_instance.gifs_search_get(api_key, 'anime', limit=1, rating='g', lang='en', offset=None, fmt=None)
        return response.data[0].images.original.url
    except ApiException as e:
        print("Exception when calling DefaultApi->gifs_search_get: %s\n" % e)
        return None

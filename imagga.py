import requests
import os
from dotenv import load_dotenv


# Load the .env file
load_dotenv()

# Access variables using os.getenv()
google_api_key = os.getenv("GOOGLE_API_KEY")


api_key = os.getenv("IMAGGA_KEY")
api_secret = os.getenv("IMAGGA_SECRET")
image_url = 'https://docs.imagga.com/static/images/docs/sample/japan-605234_1280.jpg'

response = requests.get(
    'https://api.imagga.com/v2/tags?image_url=%s' % image_url,
    auth=(api_key, api_secret))

print(response.json())

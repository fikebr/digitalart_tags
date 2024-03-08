import requests

api_key = 'acc_6c55dc8d001f7fe'
api_secret = '6d92c5afb7c090d752d23f61ebf7847f'
image_url = 'https://docs.imagga.com/static/images/docs/sample/japan-605234_1280.jpg'

response = requests.get(
    'https://api.imagga.com/v2/tags?image_url=%s' % image_url,
    auth=(api_key, api_secret))

print(response.json())

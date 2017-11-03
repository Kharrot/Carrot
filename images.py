import asyncio
import random
import configparser
import images
from imgurpython import ImgurClient

config = configparser.ConfigParser()
config.read('auth.ini')
client_id = config.get('credentials', 'client_id')
client_secret = config.get('credentials', 'client_secret')
client = ImgurClient(client_id, client_secret)

def topCommand():
    items = client.gallery()
    max_item = None
    max_views = 0
    for item in items:
        if item.views > max_views:
            max_item = item
            max_views = item.views
    return max_item

def imgCommand(tag):
    items = client.gallery_search(tag)
    if not items:
        return False
    else:
        resultimg = random.choice(items)
        return resultimg
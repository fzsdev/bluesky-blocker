from atproto import Client
from dotenv import load_dotenv
import os

load_dotenv()

username = os.getenv('USERNAME')
password = os.getenv('PASSWORD')

client = Client(base_url='https://bsky.social')
client.login(username, password)

# post = client.send_post('Test script Bluesky 01')
# print(post)

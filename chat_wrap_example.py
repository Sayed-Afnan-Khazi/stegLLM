from chat_wrap import chat_wrap
import os
from dotenv import load_dotenv
load_dotenv()

API_URL = os.environ.get('API_URL')
API_TOKEN = os.environ.get('API_TOKEN')

chat = chat_wrap(API_URL,API_TOKEN)

while True:
    prompt = input('User > ')
    res = chat.get_response(prompt)
    print("ChatBot > ",res)

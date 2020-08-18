from dotenv import load_dotenv
load_dotenv()

import os

API_TOKEN = os.getenv('API_TOKEN')

WEBHOOK_HOST = 'https://example.com'
WEBHOOK_PATH = '/webhook/' + API_TOKEN
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"
WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = os.getenv('PORT')

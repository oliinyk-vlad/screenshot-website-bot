import os

API_TOKEN = '1173239815:AAF2PNgChG-elV35VahkCiKExt04HF27_as'

WEBHOOK_HOST = 'https://example.com'
WEBHOOK_PATH = '/webhook/' + API_TOKEN
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"
WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = os.getenv('PORT')
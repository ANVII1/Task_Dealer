from dotenv  import load_dotenv
import os
load_dotenv()

# telegram bot
BOT_TOKEN = os.environ['BOT_TOKEN']

# webhook
WEBHOOK_MODE = (os.environ['WEBHOOK'] == 'True')
WEB_SERVER_HOST = os.environ['WEB_SERVER_HOST']
WEB_SERVER_PORT = os.environ['WEB_SERVER_PORT']
WEBHOOK_SSL_CERT = os.environ['PATH_TO_PEM']
WEBHOOK_SSL_PRIV = os.environ['PATH_TO_KEY']
WEBHOOK_PATH = os.environ['WEBHOOK_PATH']
BASE_WEBHOOK_URL = f"{WEB_SERVER_HOST}:{WEB_SERVER_PORT}"

# database
DB_HOST = WEBHOOK_PATH = os.environ['DB_HOST']
DB_PORT = WEBHOOK_PATH = os.environ['DB_PORT']
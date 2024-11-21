import os
import dotenv


dotenv.load_dotenv()


BOT_TOKEN = os.environ["BOT_TOKEN"]
DB_HOST = os.environ["DB_HOST"]
SANIC_HOST = os.environ["SANIC_HOST"]

PHOTO_URL_MONDAY = os.environ["PHOTO_URL_MONDAY"]
PHOTO_URL_OTHER = os.environ["PHOTO_URL_OTHER"]

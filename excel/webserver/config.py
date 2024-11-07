import os
import dotenv


dotenv.load_dotenv()


SCHEDULER_TIMEZONE = os.environ["SCHEDULER_TIMEZONE"]
ULTRA_SECRET_URL = os.environ["ULTRA_SECRET_URL"]

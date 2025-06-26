import os
from dotenv import load_dotenv
from celery.schedules import crontab


load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
SECRETE_KEY = os.getenv("SECRETE_KEY")
ALGORTITHM = os.getenv("ALGORTITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
REDIS_URL = os.getenv("REDIS_URL")
WEBHOOK = os.getenv("WEBHOOK")
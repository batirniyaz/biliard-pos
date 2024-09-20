from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET")
TG_TOKEN = os.getenv("TG_TOKEN")

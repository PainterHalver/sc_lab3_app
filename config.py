from dotenv import load_dotenv
from os import getenv, path

load_dotenv(path.join(path.dirname(__file__), '.env'))

DATABASE_URI = getenv('DATABASE_URI')
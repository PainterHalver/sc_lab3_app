from dotenv import load_dotenv
from os import getenv, path
import boto3

load_dotenv(path.join(path.dirname(__file__), ".env"))

DATABASE_USER = getenv("DATABASE_USER")
DEBUG = getenv("DEBUG")
BUCKET_NAME = getenv("BUCKET_NAME")

uri = getenv("DATABASE_URI")
uri.startswith("sqlite")

if uri.startswith("sqlite"):
    DATABASE_URI = uri
else:
    ssm = boto3.client("ssm")
    db_pass = ssm.get_parameter(Name="/app/db/password")["Parameter"]["Value"]
    DATABASE_URI = f"mysql+pymysql://{DATABASE_USER}:{db_pass}@{uri}"

import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(".env"), ".env")
load_dotenv(dotenv_path)

DB_URL = os.environ.get("DB_URL")
SECRET_CRYPTO_PASS = os.environ.get("SECRET_CRYPTO_PASS")
SECRET_JWT_PASS = os.environ.get("SECRET_JWT_PASS")
ALGORITHM = os.environ.get("ALGORITHM")

from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv
import os

load_dotenv()

## Fake Users which can use the api.
FAKE_USERS_DB = {
    "mohammad": {
        "username": "mohammad",
        "email": "mohammad@example.com",
        "hashed_password": "fakehashedsecret",
    },
    "ali": {
        "username": "ali",
        "email": "ali@example.com",
        "hashed_password": "fakehashedsecret2",
    },
}

MONGO_DB_URL = f"mongodb://{os.environ['MONGO_DB_USER']}:{os.environ['MONGO_DB_PASSWORD']}@{os.environ['MONGO_DB_HOST']}/"
MONGO_DB_DATABASE = os.environ["MONGO_DB_DATABASE"]
OAUTH2_SCHEMA = OAuth2PasswordBearer(tokenUrl="token")
CSV_FIELDS = ["FirstName", "Email", "Lastname", "Company_name"]

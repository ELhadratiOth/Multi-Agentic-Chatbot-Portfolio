from langchain_google_community.gmail.utils import build_resource_service, get_gmail_credentials
import base64
import json
from google.oauth2.service_account import Credentials
import os
from load_dotenv import load_dotenv
load_dotenv(override=True)

def get_service_account_credentials():
    encoded_key = os.getenv("SERVICE_ACCOUNT_KEY")
    print(encoded_key)

    decoded_key = base64.b64decode(encoded_key).decode("utf-8")
    print(decoded_key)
    credentials_info = json.loads(decoded_key)
    credentials = Credentials.from_service_account_info(
        credentials_info,
        scopes=["https://mail.google.com/"]
    )
    return credentials
get_service_account_credentials()
import requests
import json
import os 
from dotenv import load_dotenv



load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
CODE = os.getenv("CODE")
REFRESH_TOKEN = os.getenv("REFRESH_TOKEN")


def get_access_token():

    url = "https://accounts.zoho.in/oauth/v2/token"

    payload = {
        "refresh_token": REFRESH_TOKEN,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "refresh_token"
    }

    response = requests.post(url, data=payload)

    if response.status_code != 200:
        raise Exception(response.text)

    data = response.json()

    return data["access_token"]



#response = requests.post(url, data=payload)

#print(response.status_code)
#print(json.dumps(response.json(), indent=4))
import requests
import os
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REFRESH_TOKEN = os.getenv("REFRESH_TOKEN")


def get_access_token():

    url = "https://accounts.zoho.in/oauth/v2/token"

    payload = {
        "refresh_token": REFRESH_TOKEN,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "refresh_token"
    }

    response = requests.post(
        url,
        data=payload,
        timeout=30
    )

    print("Token API Status:", response.status_code)

    data = response.json()

    # DO NOT print the actual access token
    if response.status_code != 200:
        raise Exception(
            f"Token refresh failed: {data}"
        )

    if "access_token" not in data:
        raise Exception(
            f"No access token returned: {data}"
        )

    print("New access token received")
    print("Expires in:", data.get("expires_in"))

    return data["access_token"]


if __name__ == "__main__":
    token = get_access_token()
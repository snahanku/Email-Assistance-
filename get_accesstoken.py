import requests
import json

CLIENT_ID = "1000.HJDQV1S5GOF9C0WO3MQ1X782WFPRHJ"
CLIENT_SECRET = "a8106587d14ffcc3302faddf1b46971e2394cf8655"
GRANT_TOKEN = "1000.c1dd8ebd357b4057a59537665e6281f8.586e03f815138eb2c2e7f42c597c3678"

url = "https://accounts.zoho.in/oauth/v2/token"

payload = {
    "grant_type": "authorization_code",
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
    "code": GRANT_TOKEN
}

response = requests.post(url, data=payload)

print("Status Code:", response.status_code)
print(json.dumps(response.json(), indent=4))
import requests
import json
from refreshtoken import get_access_token
ACCESS_TOKEN = get_access_token()

headers = {
    "Authorization": f"Zoho-oauthtoken {ACCESS_TOKEN}"
}

url = "https://mail.zoho.in/api/accounts"

response = requests.get(url, headers=headers)

print("Status:", response.status_code)
print(json.dumps(response.json(), indent=4))
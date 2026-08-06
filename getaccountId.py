import requests
import json
from refreshtoken import get_access_token


ACCESS_TOKEN = get_access_token()


def get_account_id():

    url = "https://mail.zoho.in/api/accounts"

    headers = {
    "Authorization": f"Zoho-oauthtoken {ACCESS_TOKEN}"
}

    response = requests.get(url, headers=headers)

    #print(response.status_code)
    #print(json.dumps(response.json(), indent=4))
    data = response.json()
    return data["data"][0]["accountId"]
    

#data = get_account_id()
#print(data.json())

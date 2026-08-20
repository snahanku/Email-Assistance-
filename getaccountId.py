#import requests
#import json
#from refreshtoken import get_access_token


##ACCESS_TOKEN = get_access_token()
##url = "https://mail.zoho.in/api/accounts"

##headers = {
   ##"Authorization": f"Zoho-oauthtoken {ACCESS_TOKEN}"
##}

##def get_account_id():

   ## url = "https://mail.zoho.in/api/accounts"

  ##  headers = {
   ## "Authorization": f"Zoho-oauthtoken {ACCESS_TOKEN}"
##}

   ## response = requests.get(url, headers=headers)

    #print(response.status_code)
    #print(json.dumps(response.json(), indent=4))
   ## data = response.json()
   ## return data["data"][0]["accountId"]
    

#data = get_account_id()
#print(data.json())


####def get_account_id():

    ##response = requests.get(
        ##url,
        ##headers=headers
    ##)

    ##print("Account API Status:", response.status_code)
    ##print("Account API Response:", response.text)

    ##data = response.json()

    ##print("Parsed Data:", data)
    ##print("Data Type:", type(data.get("data")))

   ## return data["data"][0]["accountId"]



##acc = get_account_id()
##print("Account ID:", acc)




import requests
import json
from refreshtoken import get_access_token


def get_account_id():
    """Fetch account ID from Zoho Mail API with fresh token each time."""
    
    # Get a FRESH token each time (don't reuse stale one)
    access_token = get_access_token()
    
    url = "https://mail.zoho.in/api/accounts"
    headers = {
        "Authorization": f"Zoho-oauthtoken {access_token}"
    }
    
    response = requests.get(url, headers=headers)
    
    print("Account API Status:", response.status_code)
    print("Account API Response:", response.text)
    
    # ⚠️ ERROR HANDLING - Check status BEFORE accessing data
    if response.status_code != 200:
        raise Exception(
            f"Failed to fetch account ID: {response.status_code} - {response.text}"
        )
    
    data = response.json()
    
    print("Parsed Data:", data)
    print("Data Type:", type(data.get("data")))
    
    # Verify data["data"] exists and is a list
    if not isinstance(data.get("data"), list):
        raise Exception(
            f"Unexpected response structure: {data}"
        )
    
    if len(data["data"]) == 0:
        raise Exception("No accounts found in response")
    
    return data["data"][0]["accountId"]


if __name__ == "__main__":
    acc = get_account_id()
    print("Account ID:", acc)










import requests
import os 
from dotenv import load_dotenv
from refreshtoken import get_access_token
load_dotenv()
#ACCOUNT_ID =  "1712401000000002002"
ACCOUNT_ID = os.getenv("ACCOUNT_ID")

url = f"https://mail.zoho.in/api/accounts/{ACCOUNT_ID}/messages/view?limit=50&start=0"
#ACCESS_TOKEN = "1000.55dffc831d215d14345f1d2878c63b2c.bbf6788b1bc361a983c217be8feea236"
ACCESS_TOKEN = get_access_token()

headers = {
    "Authorization": f"Zoho-oauthtoken {ACCESS_TOKEN}"
}
response = requests.get(url, headers=headers)
emails = response.json().get("data", [])

for email in emails:
    Email_details = {

        "From": email.get("sender", ""),
        "FromAddress" : email.get("fromAddress" , ""),
        #"To": str_to_address(
         #   email.get("toAddress", "")
       # ),

        "Subject": email.get("subject", ""),

        "Body": email.get("summary", ""),
        "CC": email.get("ccAddress", ""),
        "BCC" : email.get("bcAddress", ""),
        # Uncomment when LLM is enabled
        
        #"Priority": llm_output["urgency"],
        #"Summary": llm_output["summary"],
        #"Positive_Reply_Suggestion": llm_output["reply"]["very_positive"],
        #"Professional_Reply_Suggestion": llm_output["reply"]["professional"],
        #"Firm_Reply_Suggestion": llm_output["reply"]["slightly_frustrated"]
    }

    print(Email_details)

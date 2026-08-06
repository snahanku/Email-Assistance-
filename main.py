import requests
import json
import html
import re
import os
from llm import analyze_email
from refreshtoken import get_access_token
from getaccountId import  get_account_id
from dotenv import load_dotenv

load_dotenv()


# from llm import analyze_email


ACCESS_TOKEN = get_access_token()
ACCOUNT_ID =  get_account_id()


WEB_APP_URL = os.getenv("WEB_APP_URL")

# Fetch multiple emails
url = f"https://mail.zoho.in/api/accounts/{ACCOUNT_ID}/messages/view?limit=50&start=0"

headers = {
    "Authorization": f"Zoho-oauthtoken {ACCESS_TOKEN}"
}


# -----------------------------
# Remove HTML from email address
# -----------------------------
def str_to_address(email_address: str) -> str:
    decoded = html.unescape(email_address)

    match = re.search(r"<([^>]+)>", decoded)

    if match:
        return match.group(1)

    return decoded

def check_bcc(bcc_address) -> str :
    if bcc_address == '': 
        return "Not Provided"
    else:
        return bcc_address

# -----------------------------
# Load processed message IDs
# -----------------------------
PROCESSED_FILE = "processed_ids.json"

if os.path.exists(PROCESSED_FILE):
    with open(PROCESSED_FILE, "r") as f:
        processed_ids = set(json.load(f))
else:
    processed_ids = set()


# -----------------------------
# Fetch emails
# -----------------------------
response = requests.get(url, headers=headers)

print("Status:", response.status_code)

if response.status_code != 200:
    print(response.text)
    exit()

emails = response.json().get("data", [])
#print(emails)

print(f"Found {len(emails)} emails")


# -----------------------------
# Process every new email
# -----------------------------
for email in emails:

    message_id = email.get("messageId")

    # Skip already processed emails
    if message_id in processed_ids:
        continue

    print(f"Processing : {message_id}")

    email_body = email.get("summary", "")

    # Uncomment once LLM quota is back
    print(email_body)
    response = analyze_email(email_body)
    print(response)
    llm_output = json.loads(response)

    Email_details = {

        "From": email.get("sender", ""),
        "FromAddress" : email.get("fromAddress" , ""),
        "CC": str_to_address(email.get("ccAddress", "")),
        "BCC": check_bcc(str_to_address(email.get("bcAddress", ""))),
        "To": str_to_address(
            email.get("toAddress", "")
        ),

        "Subject": email.get("subject", ""),

        "Body": email.get("summary", ""),

        # Uncomment when LLM is enabled
        
        "Priority": llm_output["urgency"],
        "Summary": llm_output["summary"],
        "Positive_Reply_Suggestion": llm_output["reply"]["very_positive"],
        "Professional_Reply_Suggestion": llm_output["reply"]["professional"],
        "Firm_Reply_Suggestion": llm_output["reply"]["slightly_frustrated"]
    }

    print(Email_details)

    gsheet_response = requests.post(
        WEB_APP_URL,
        json=Email_details
    )

    print(gsheet_response.status_code)
    print(gsheet_response.text)

    # Save processed ID only if upload succeeded
    if gsheet_response.status_code == 200:
        processed_ids.add(message_id)


# -----------------------------
# Save processed IDs
# -----------------------------
with open(PROCESSED_FILE, "w") as f:
    json.dump(list(processed_ids), f, indent=4)
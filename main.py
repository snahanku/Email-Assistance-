import requests
import json
import html
import re
import os
import sys
from llm import analyze_email
from refreshtoken import get_access_token
from getaccountId import get_account_id
from dotenv import load_dotenv

load_dotenv()

PROCESSED_FILE = "processed_ids.json"
WEB_APP_URL = os.getenv("WEB_APP_URL")

# Helper functions
def str_to_address(email_address: str) -> str:
    if not email_address:
        return ""
    decoded = html.unescape(email_address)
    match = re.search(r"<([^>]+)>", decoded)
    return match.group(1) if match else decoded

def check_bcc(bcc_address: str) -> str:
    return "Not Provided" if not bcc_address else bcc_address


def run_cron_job():
    print("🚀 Starting scheduled email processing job...")
    
    # 1. Load Tokens Dynamically
    ACCESS_TOKEN = get_access_token()
    ACCOUNT_ID = get_account_id()

    if not ACCESS_TOKEN or not ACCOUNT_ID:
        print("❌ Error: Could not fetch ACCESS_TOKEN or ACCOUNT_ID.")
        sys.exit(1)

    # 2. Fetch processed IDs
    processed_ids = set()
    if os.path.exists(PROCESSED_FILE):
        try:
            with open(PROCESSED_FILE, "r") as f:
                processed_ids = set(json.load(f))
        except Exception as e:
            print(f"⚠️ Warning loading processed IDs: {e}")

    # 3. Fetch emails from Zoho
    url = f"https://mail.zoho.in/api/accounts/{ACCOUNT_ID}/messages/view?limit=50&start=0"
    headers = {"Authorization": f"Zoho-oauthtoken {ACCESS_TOKEN}"}

    try:
        response = requests.get(url, headers=headers)
        
        # Check HTTP Status
        if response.status_code != 200:
            print(f"❌ Zoho returned HTTP status {response.status_code}: {response.text[:200]}")
            sys.exit(1)

        # Check if response is actually JSON (Prevents HTML crash)
        content_type = response.headers.get("Content-Type", "")
        if "application/json" not in content_type:
            print("❌ Zoho returned an HTML response instead of JSON. Skipping cycle.")
            sys.exit(1)

        emails = response.json().get("data", [])
        print(f"Found {len(emails)} emails in inbox.")

    except Exception as e:
        print(f"❌ Network/Fetch error: {e}")
        sys.exit(1)

    # 4. Process new emails
    new_processed_count = 0
    for email in emails:
        message_id = email.get("messageId")

        if message_id in processed_ids:
            continue

        print(f"Processing message ID: {message_id}")
        email_body = email.get("summary", "")

        try:
            response_text = analyze_email(email_body)
            llm_output = json.loads(response_text)

            Email_details = {
                "From": email.get("sender", ""),
                "FromAddress": email.get("fromAddress", ""),
                "CC": str_to_address(email.get("ccAddress", "")),
                "BCC": check_bcc(str_to_address(email.get("bcAddress", ""))),
                "To": str_to_address(email.get("toAddress", "")),
                "Subject": email.get("subject", ""),
                "Body": email_body,
                "Priority": llm_output.get("urgency", "Normal"),
                "Summary": llm_output.get("summary", ""),
                "Positive_Reply_Suggestion": llm_output.get("reply", {}).get("very_positive", ""),
                "Professional_Reply_Suggestion": llm_output.get("reply", {}).get("professional", ""),
                "Firm_Reply_Suggestion": llm_output.get("reply", {}).get("slightly_frustrated", "")
            }

            if WEB_APP_URL:
                gsheet_response = requests.post(WEB_APP_URL, json=Email_details)
                if gsheet_response.status_code == 200:
                    processed_ids.add(message_id)
                    new_processed_count += 1
            else:
                print("⚠️ WEB_APP_URL not set in environment!")

        except Exception as e:
            print(f"❌ Failed to process email {message_id}: {e}")

    # 5. Save updated processed IDs back to JSON
    with open(PROCESSED_FILE, "w") as f:
        json.dump(list(processed_ids), f, indent=4)

    print(f"✅ Job complete. Processed {new_processed_count} new email(s).")

if __name__ == "__main__":
    run_cron_job()
import requests
import json
import html
import re
import os
import time
from dotenv import load_dotenv

from llm import analyze_email
from refreshtoken import get_access_token
from getaccountId import get_account_id

from processed_db import (
    initialize_database,
    is_processed,
    mark_processed
)
load_dotenv()

WEB_APP_URL = os.getenv("WEB_APP_URL")

PROCESSED_FILE = "processed_ids.json"



# ---------------------------------------------------------
# Utility Functions
# ---------------------------------------------------------

def str_to_address(email_address: str) ->str:
    decoded = html.unescape(email_address)

    match = re.search(r"<([^>]+)>", decoded)

    if match:
        return match.group(1)

    return decoded


def check_bcc(bcc_address: str) -> str:
    if not bcc_address:
        return "Not Provided"
    return bcc_address


# ---------------------------------------------------------
# Processed IDs
# ---------------------------------------------------------

def load_processed_ids():

    if os.path.exists(PROCESSED_FILE):
        with open(PROCESSED_FILE, "r") as f:
            return set(json.load(f))

    return set()


def save_processed_ids(processed_ids):

    with open(PROCESSED_FILE, "w") as f:
        json.dump(list(processed_ids), f, indent=4)


# ---------------------------------------------------------
# Main Email Processing Function
# ---------------------------------------------------------

def process_emails():
    
    print("=" * 60)
    print("Checking for new emails...")
    print("=" * 60)

    processed_ids = load_processed_ids()

    # Fresh token every cycle
    access_token = get_access_token()
    account_id = get_account_id()
     
    url = (
        f"https://mail.zoho.in/api/accounts/"
        f"{account_id}/messages/view?limit=50&start=0"
    )

    headers = {
        "Authorization": f"Zoho-oauthtoken {access_token}"
    }

    response = requests.get(url, headers=headers)

    print("Status Code :", response.status_code)

    if response.status_code != 200:
        print("Unable to fetch emails.")
        print(response.text)
        return

    emails = response.json().get("data", [])

    print(f"Found {len(emails)} emails.")

    for email in emails:

        message_id = email.get("messageId")

        if message_id in processed_ids:
            continue

        print(f"\nProcessing Email : {message_id}")

        try:

            email_body = email.get("summary", "")

            llm_response = analyze_email(email_body)
            llm_output = json.loads(llm_response)

            email_details = {

                "From": email.get("sender", ""),

                "FromAddress": email.get(
                    "fromAddress",
                    ""
                ),

                "CC": str_to_address(
                    email.get(
                        "ccAddress",
                        ""
                    )
                ),

                "BCC": check_bcc(
                    str_to_address(
                        email.get(
                            "bcAddress",
                            ""
                        )
                    )
                ),

                "To": str_to_address(
                    email.get(
                        "toAddress",
                        ""
                    )
                ),

                "Subject": email.get(
                    "subject",
                    ""
                ),

                "Body": email_body,

                "Priority": llm_output["urgency"],

                "Summary": llm_output["summary"],

                "Positive_Reply_Suggestion":
                    llm_output["reply"]["very_positive"],

                "Professional_Reply_Suggestion":
                    llm_output["reply"]["professional"],

                "Firm_Reply_Suggestion":
                    llm_output["reply"]["slightly_frustrated"]

            }
            print(email_details)
            print("Uploading to Google Sheet...")

            gsheet_response = requests.post(
                WEB_APP_URL,
                json=email_details
            )

            print("Google Sheet Status:",
                  gsheet_response.status_code)

            if gsheet_response.status_code == 200:

                processed_ids.add(message_id)
                save_processed_ids(processed_ids)
                #mark_processed(message_id)
                print("Successfully Uploaded")

            else:

                print("Upload Failed")
                print(gsheet_response.text)

        except Exception as e:

            print(f"Error processing {message_id}")
            print(e)

    print("\nCycle Completed.")


# ---------------------------------------------------------
# Infinite Runner
# ---------------------------------------------------------

if __name__ == "__main__":

    while True:

        try:

            process_emails()

        except Exception as e:

            print("\nUnexpected Error")
            print(e)

        print("\nSleeping for 5 minutes...\n")

        time.sleep(300)
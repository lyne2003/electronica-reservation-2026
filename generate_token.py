"""
Run this script ONCE locally to generate a fresh Google Calendar OAuth token.

Steps:
1. Make sure you have a 'credentials.json' file in this folder
   (download it from Google Cloud Console → APIs & Services → Credentials → OAuth 2.0 Client → Download JSON)
   OR paste your CALENDAR_CREDS_JSON content into a file named 'credentials.json'

2. Run:  python generate_token.py

3. A browser window will open — log in with the Google account that owns the calendar.

4. After login, a 'token.json' file will be created in this folder.

5. Copy the ENTIRE content of token.json and paste it into Render's
   environment variable: CALENDAR_TOKEN_JSON
"""

import json
import os
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

SCOPES = ["https://www.googleapis.com/auth/calendar"]

def main():
    creds = None

    # Check if token.json already exists
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    # If no valid credentials, run the OAuth flow
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the token
        with open("token.json", "w") as token_file:
            token_file.write(creds.to_json())

    print("\n✅ Token generated successfully!")
    print("\n📋 Copy the content below and paste it into Render's CALENDAR_TOKEN_JSON environment variable:\n")
    with open("token.json", "r") as f:
        content = f.read()
    print(content)
    print("\n✅ Done! Update CALENDAR_TOKEN_JSON on Render with the above JSON.")

if __name__ == "__main__":
    main()

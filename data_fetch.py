import os
import json
import gspread
import pandas as pd
from google.oauth2.service_account import Credentials

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

def authorize_google_sheet():
    try:
        creds_info = os.getenv("GOOGLE_CREDENTIALS_JSON")

        if creds_info:
            # Render: Load from environment
            creds = Credentials.from_service_account_info(json.loads(creds_info), scopes=SCOPES)
        else:
            # Local: Load from file
            with open("credentials.json", "r") as f:
                creds_json = json.load(f)
            creds = Credentials.from_service_account_info(creds_json, scopes=SCOPES)

        client = gspread.authorize(creds)
        return client

    except Exception as e:
        print(" Error authorizing Google Sheets API:", e)
        return None

def fetch_vendor_data(sheet_key, worksheet_name="Form responses 1"):
    client = authorize_google_sheet()
    if client is None:
        return pd.DataFrame()

    try:
        sheet = client.open_by_key(sheet_key)
        worksheet = sheet.worksheet(worksheet_name)
        data = worksheet.get_all_records()
        df = pd.DataFrame(data)

        # Clean column names
        df.columns = df.columns.str.strip()
        df.columns = df.columns.str.replace("–", "-", regex=False)
        df.columns = df.columns.str.replace("’", "'", regex=False)

        return df

    except Exception as e:
        print(" Error fetching data from Google Sheet:", e)
        return pd.DataFrame()

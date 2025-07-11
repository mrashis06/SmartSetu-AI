import os
import json
import gspread
import pandas as pd
from google.oauth2.service_account import Credentials

# --- Google API Scopes ---
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

def authorize_google_sheet():
    try:
        # --- Try Render first: Read from environment variable
        creds_json_str = os.getenv("GOOGLE_CREDENTIALS_JSON")

        if creds_json_str:
            creds_dict = json.loads(creds_json_str.replace("\\n", "\n"))  # Fix escaped newlines
        else:
            # --- Fallback to local credentials.json
            with open("credentials.json", "r") as f:
                creds_dict = json.load(f)

        creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
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

# --- Local Testing Block ---
if __name__ == "__main__":
    SHEET_KEY = "1ccQAGRSCcJbJijorbBzSwU-wx60Ftf-2lzayKzCZQRw"
    df = fetch_vendor_data(SHEET_KEY)

    if df.empty:
        print(" No data fetched.")
    else:
        print(" Vendor data fetched successfully:")
        print(df.head())

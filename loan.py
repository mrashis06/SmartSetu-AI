# loan.py

def determine_loan_offer(credit_score):
    if credit_score >= 80:
        return 100000, 4
    elif credit_score >= 60:
        return 50000, 6
    elif credit_score >= 40:
        return 20000, 8
    elif credit_score >= 30:
        return 10000, 10
    else:
        return 0, 0

def calculate_emi(loan_amount, months, interest_rate):
    total_repayment = loan_amount + (loan_amount * interest_rate * months / (12 * 100))
    emi = round(total_repayment / months, 2)
    return emi, round(total_repayment)
#calculator.py
import numpy as np

def calculate_credit_score(transactions, consistency, supplier_verified, testimonials, max_txn):
    supplier_val = 100 if str(supplier_verified).strip().lower() == "yes" else 0
    testimonial_score = (testimonials / 10) * 100
    normalized_txn = (transactions / max_txn) * 100 if max_txn > 0 else 0

    score = (
        0.4 * normalized_txn +
        0.3 * consistency +
        0.2 * supplier_val +
        0.1 * testimonial_score
    )

    return round(min(100, max(0, score)), 2)

def calculate_risk_score(expenses, avg_income):
    if avg_income == 0:
        return 100
    variance = np.std(expenses)
    return round((variance / avg_income) * 100, 2)

def get_risk_level(score):
    if score < 20:
        return "Low Risk"
    elif score <= 50:
        return "Medium Risk"
    else:
        return "High Risk"
#data_fetch
import os
import json
import gspread
import pandas as pd
from google.oauth2.service_account import Credentials

SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']

def authorize_google_sheet():
    try:
        creds_info = os.getenv("GOOGLE_CREDENTIALS_JSON")

        if creds_info:
           creds = Credentials.from_service_account_info(json.loads(creds_info), scopes=SCOPES)
        else:
           creds = Credentials.from_service_account_file("credentials.json", scopes=SCOPES)
           
        client = gspread.authorize(creds)
        return client

    except Exception as e:
        print("Error authorizing Google Sheets API:", e)
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

        # Clean column names to avoid weird characters or spaces
        df.columns = df.columns.str.strip()
        df.columns = df.columns.str.replace("–", "-", regex=False)
        df.columns = df.columns.str.replace("’", "'", regex=False)

        return df
    except Exception as e:
        print("Error fetching data from Google Sheet:", e)
        return pd.DataFrame()

# Test run block for local testing; remove or comment out when deploying
if __name__ == "__main__":
    SHEET_KEY = "1ccQAGRSCcJbJijorbBzSwU-wx60Ftf-2lzayKzCZQRw"
    df = fetch_vendor_data(SHEET_KEY)

    if df.empty:
        print("No data fetched.")
    else:
        print("Vendor data fetched successfully:")
        print(df.head())

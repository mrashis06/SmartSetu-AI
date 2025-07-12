from datetime import datetime
import streamlit as st
import pandas as pd
import sys
import os
import json
import gspread
import random
import string
from google.oauth2.service_account import Credentials

# --- Local imports ---
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from calculator import calculate_credit_score, calculate_risk_score, get_risk_level
from color_utils import get_score_color, get_level_color

# --- Google Sheet Config ---
SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
SHEET_KEY = "1ccQAGRSCcJbJijorbBzSwU-wx60Ftf-2lzayKzCZQRw"

# --- Vendor Code Generator ---
def generate_unique_vendor_code(name, worksheet):
    prefix = ''.join(e for e in name.upper() if e.isalnum())[:3]
    existing_codes = worksheet.col_values(3)  # Column 3: Vendor Code
    while True:
        suffix = ''.join(random.choices(string.digits, k=4))
        code = prefix + suffix
        if code not in existing_codes:
            return code

# --- Worksheet Access ---
def get_worksheet():
    creds_info = os.getenv("GOOGLE_CREDENTIALS_JSON")

    if creds_info:
        creds = Credentials.from_service_account_info(json.loads(creds_info), scopes=SCOPES)
    else:
        with open("credentials.json", "r") as f:
            creds_json = json.load(f)
        creds = Credentials.from_service_account_info(creds_json, scopes=SCOPES)

    client = gspread.authorize(creds)
    return client.open_by_key(SHEET_KEY).sheet1

# --- Page Setup ---
st.set_page_config(page_title="Vendor Registration | SmartSetu-AI", layout="wide")
with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
with open("templates/header.html") as f:
    st.markdown(f.read(), unsafe_allow_html=True)

st.title(" Vendor Registration & Credit Prediction")

# --- Persist inputs until refresh ---
if "submitted" not in st.session_state:
    st.session_state["submitted"] = False

# --- Entry Form ---
with st.form("vendor_form"):
    st.subheader("Enter Vendor Details")

    name = st.text_input("Enter Your Name", value=st.session_state.get("name", ""))
    transactions = st.number_input("Monthly Transactions", min_value=0.0, value=st.session_state.get("transactions", 0.0))
    income1 = st.number_input("Monthly Income - Month 1", min_value=0.0, value=st.session_state.get("income1", 0.0))
    income2 = st.number_input("Monthly Income - Month 2", min_value=0.0, value=st.session_state.get("income2", 0.0))
    income3 = st.number_input("Monthly Income - Month 3", min_value=0.0, value=st.session_state.get("income3", 0.0))
    expense1 = st.number_input("Spending Variance - Month 1", min_value=0.0, value=st.session_state.get("expense1", 0.0))
    expense2 = st.number_input("Spending Variance - Month 2", min_value=0.0, value=st.session_state.get("expense2", 0.0))
    expense3 = st.number_input("Spending Variance - Month 3", min_value=0.0, value=st.session_state.get("expense3", 0.0))

    supplier_verified = st.selectbox("Supplier Verified", ["Yes", "No"])
    consistency = st.slider("Consistency Score (0-100)", 0, 100, 50)
    testimonials = st.slider("Customer Testimonial (0-10)", 0, 10, 5)

    submitted = st.form_submit_button("Predict & Save")

# --- Optional Refresh Button ---
if st.button(" Reset Form"):
    for key in ["submitted", "name", "transactions", "income1", "income2", "income3",
                "expense1", "expense2", "expense3"]:
        if key in st.session_state:
            del st.session_state[key]
    st.rerun()


# --- On Submit ---
if submitted:
    with st.spinner("Calculating scores and saving data..."):
        avg_income = (income1 + income2 + income3) / 3
        expenses = [expense1, expense2, expense3]
        max_txn = transactions

        credit_score = calculate_credit_score(transactions, consistency, supplier_verified, testimonials, max_txn)
        risk_score = calculate_risk_score(expenses, avg_income)
        risk_level = get_risk_level(risk_score)

        credit_color = get_score_color(credit_score)
        risk_color = get_score_color(risk_score, kind="risk")
        level_color = get_level_color(risk_level)

        st.markdown("### Prediction Result")
        st.markdown(f"""
        <div style='background-color:#000000; padding:16px; border-radius:12px;'>
            <p style='color:white;'>Credit Score: <span style='color:{credit_color}; font-weight:bold;'>{credit_score}</span></p>
            <p style='color:white;'>Risk Score: <span style='color:{risk_color}; font-weight:bold;'>{risk_score}</span></p>
            <p style='color:white;'>Risk Level: <span style='color:{level_color}; font-weight:bold;'>{risk_level}</span></p>
        </div>
        """, unsafe_allow_html=True)

        try:
            worksheet = get_worksheet()
            vendor_code = generate_unique_vendor_code(name, worksheet)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            worksheet.append_row([
                timestamp,
                name,
                vendor_code,
                transactions,
                income1, income2, income3,
                expense1, expense2, expense3,
                supplier_verified,
                consistency,
                testimonials
            ])

            # Save to session state
            st.session_state["submitted"] = True
            st.session_state["name"] = name
            st.session_state["transactions"] = transactions
            st.session_state["income1"] = income1
            st.session_state["income2"] = income2
            st.session_state["income3"] = income3
            st.session_state["expense1"] = expense1
            st.session_state["expense2"] = expense2
            st.session_state["expense3"] = expense3

            # Spacing
            st.markdown("<br>", unsafe_allow_html=True)

            st.markdown("""
            <div style="background-color:#144d38; padding:12px; border-radius:10px;">
                <p style="color:white; font-size:16px; margin:0;"> Data successfully saved!</p>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            st.markdown(f"""
            <div style="background-color:#144d38; padding:14px; border-radius:10px;">
                <p style="color:white; font-size:18px; margin:0;">
                 Your <b>Vendor Code</b>: <span style="font-size:20px;">{vendor_code}</span><br>
                 Save this to access your prediction report later!
                </p>
            </div>
            """, unsafe_allow_html=True)

            st.balloons()

        except Exception as e:
            st.error(f" Failed to save data: {e}")

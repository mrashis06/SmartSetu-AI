# credit_predictor.py

import streamlit as st
import pandas as pd
import os
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

from data_fetch import fetch_vendor_data
from calculator import calculate_credit_score, calculate_risk_score, get_risk_level
from loan import determine_loan_offer, calculate_emi
from color_utils import get_score_color, get_level_color

# --- Page Config & Styling ---
st.set_page_config(page_title="Credit Report | SmartSetu-AI", layout="wide")
with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
with open("templates/header.html") as f:
    st.markdown(f.read(), unsafe_allow_html=True)

# --- Session state for vendor code ---
if "vendor_code_input" not in st.session_state:
    st.session_state.vendor_code_input = ""

# --- Header with Refresh Button ---
col1, col2 = st.columns([8, 1])
with col1:
    st.markdown("## Vendor Credit Lookup")
with col2:
    if st.button(" Refresh", key="refresh_button_top"):
        st.session_state.vendor_code_input = ""
        st.rerun()


st.markdown("<br>", unsafe_allow_html=True)

# --- Data Load ---
SHEET_KEY = "1ccQAGRSCcJbJijorbBzSwU-wx60Ftf-2lzayKzCZQRw"
df = fetch_vendor_data(SHEET_KEY)

# --- Vendor Code Input ---
code_input = st.text_input("Enter your Vendor Code:", value=st.session_state.vendor_code_input)
st.session_state.vendor_code_input = code_input  # Update session

# --- Lookup Validation ---
if code_input:
    if "Vendor Code" not in df.columns:
        st.error(" 'Vendor Code' column missing in Google Sheet.")
        st.stop()

    row = df[df["Vendor Code"] == code_input.upper()]
    if row.empty:
        st.error(" Invalid Vendor Code. Please try again.")
        st.stop()

    vendor = row.iloc[0]
    name = vendor['Name of Vendor']

    # --- Score Calculations ---
    txns = float(vendor["Monthly Transactions"])
    incomes = [float(vendor[f"Monthly Income - Month {i}"]) for i in range(1, 4)]
    expenses = [float(vendor[f"Spending Variance - Month {i}"]) for i in range(1, 4)]
    supplier_verified = vendor["Supplier Verified"]
    consistency = float(vendor["Consistency Score"])
    testimonials = float(vendor["Customer Testimonial"])
    avg_income = sum(incomes) / 3

    credit_score = calculate_credit_score(txns, consistency, supplier_verified, testimonials, txns)
    risk_score = calculate_risk_score(expenses, avg_income)
    risk_level = get_risk_level(risk_score)

    # --- Display Metrics ---
    credit_color = get_score_color(credit_score)
    risk_color = get_score_color(risk_score, kind="risk")
    level_color = get_level_color(risk_level)

    st.markdown(f"###  Report for: `{name}`")
    st.markdown(f"""
    <div style='background-color:#000000; padding:16px; border-radius:12px;'>
        <p style='color:white;'>Credit Score: <span style='color:{credit_color}'><b>{credit_score}</b></span></p>
        <p style='color:white;'>Risk Score: <span style='color:{risk_color}'><b>{risk_score}</b></span></p>
        <p style='color:white;'>Risk Level: <span style='color:{level_color}'><b>{risk_level}</b></span></p>
    </div>
    """, unsafe_allow_html=True)

    # --- Loan Eligibility ---
    loan_amt, interest = determine_loan_offer(credit_score)
    if loan_amt > 0:
        st.success(f" Eligible for loan of ₹{loan_amt:,} at {interest}% interest")
        custom_loan = st.slider("Select Loan Amount", 1000, loan_amt, step=1000)
        duration = st.slider("Select Duration (Months)", 6, 24, 12)
        emi, total = calculate_emi(custom_loan, duration, interest)

        st.markdown(f"""
        - **Loan Amount:** ₹{custom_loan:,}
        - **Interest Rate:** {interest}%
        - **Duration:** {duration} months
        - **Monthly EMI:** ₹{emi:,}
        - **Total Repayment:** ₹{round(total):,}
        """)
    else:
        st.error(" Not eligible for a loan based on the credit score.")

    # --- PDF Report Generation ---
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    p.setFont("Helvetica", 12)
    y = 750
    p.drawString(100, y, "SmartSetu-AI Vendor Credit Report")
    y -= 30
    p.drawString(100, y, f"Name: {name}")
    y -= 20
    p.drawString(100, y, f"Vendor Code: {code_input}")
    y -= 20
    p.drawString(100, y, f"Credit Score: {credit_score}")
    y -= 20
    p.drawString(100, y, f"Risk Score: {risk_score}")
    y -= 20
    p.drawString(100, y, f"Risk Level: {risk_level}")
    y -= 20
    if loan_amt > 0:
        p.drawString(100, y, f"Loan Eligible: ₹{loan_amt:,} @ {interest}%")
        y -= 20
        p.drawString(100, y, f"EMI: ₹{emi:,} | Total Repayment: ₹{round(total):,}")
    else:
        p.drawString(100, y, "Loan Eligible: No")
    p.save()
    buffer.seek(0)

    st.download_button(
        label=" Download PDF Report",
        data=buffer,
        file_name=f"{name}_CreditReport.pdf",
        mime="application/pdf"
    )

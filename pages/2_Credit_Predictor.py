import streamlit as st
import pandas as pd
from loan import determine_loan_offer, calculate_emi
from data_fetch import fetch_vendor_data
from calculator import calculate_credit_score, calculate_risk_score, get_risk_level

st.set_page_config(page_title="Credit Score Predictor", layout="wide")

# Load CSS and Header
with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
with open("templates/header.html") as f:
    st.markdown(f.read(), unsafe_allow_html=True)

with st.container():
    st.title(" Credit Score Predictor")

    # Fetch & Process Data
    SHEET_KEY = "1ccQAGRSCcJbJijorbBzSwU-wx60Ftf-2lzayKzCZQRw"
    df = fetch_vendor_data(SHEET_KEY)

    if df.empty:
        st.warning("No vendor data available.")
        st.stop()

    # Vendor Selection
    st.sidebar.title("Select Vendor")
    selected_vendor = st.sidebar.selectbox("Choose a Vendor:", df["Name of Vendor"].tolist())
    row = df[df["Name of Vendor"] == selected_vendor].iloc[0]

    # Score Calculation
    transactions = float(row['Monthly Transactions'])
    consistency = float(row['Consistency Score'])
    supplier_verified = row['Supplier Verified']
    testimonials = float(row['Customer Testimonial'])
    income1 = float(row['Monthly Income - Month 1'])
    income2 = float(row['Monthly Income - Month 2'])
    income3 = float(row['Monthly Income - Month 3'])
    avg_income = (income1 + income2 + income3) / 3
    expenses = [
        float(row['Spending Variance - Month 1']),
        float(row['Spending Variance - Month 2']),
        float(row['Spending Variance - Month 3']),
    ]

    max_txn = df['Monthly Transactions'].max()
    credit_score = calculate_credit_score(transactions, consistency, supplier_verified, testimonials, max_txn)
    risk_score = calculate_risk_score(expenses, avg_income)
    risk_level = get_risk_level(risk_score)

    # Display Scores
    st.subheader(" Vendor Credit Evaluation")
    st.metric("Credit Score", credit_score)
    st.metric("Risk Score", risk_score)
    st.metric("Risk Level", risk_level)

    # Loan Eligibility
    st.subheader(" Loan Eligibility & Repayment Details")
    loan_amount, interest_rate = determine_loan_offer(credit_score)

    if loan_amount > 0:
        st.success(f"Eligible for loan of ₹{loan_amount:,} at {interest_rate}% interest")

        st.markdown("####  Simulate Your Loan Repayment")
        custom_loan = st.slider("Select Loan Amount (₹)", 1000, loan_amount, step=1000)
        custom_months = st.slider("Select Duration (Months)", 6, 24, value=12)

        emi, total = calculate_emi(custom_loan, custom_months, interest_rate)

        st.markdown(f"""
        - **Loan Amount:** ₹{custom_loan:,}
        - **Interest Rate:** {interest_rate}%
        - **Duration:** {custom_months} months
        - **Monthly EMI:** ₹{emi:,}
        - **Total Repayment:** ₹{round(total):,}
        """)
    else:
        st.error("Not eligible for a loan based on the credit score.")

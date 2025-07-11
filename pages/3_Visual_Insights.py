import streamlit as st
import pandas as pd
from data_fetch import fetch_vendor_data
from charts import (
    draw_vendor_pie_chart,
    draw_vendor_line_chart,
    draw_vendor_bar_chart
)
from calculator import calculate_credit_score, calculate_risk_score, get_risk_level

# --- Page Setup ---
st.set_page_config(page_title="Your Credit Insights", layout="wide")

with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
with open("templates/header.html") as f:
    st.markdown(f.read(), unsafe_allow_html=True)

# --- Title & Refresh Button ---
col1, col2 = st.columns([6, 1])
with col1:
    st.title(" Visual Insights for your credit report")
with col2:
    if st.button(" Refresh"):
        st.session_state.vendor_code = ""
        st.rerun()

# --- Session State Setup ---
if "vendor_code" not in st.session_state:
    st.session_state.vendor_code = ""

# --- Google Sheet Fetch ---
SHEET_KEY = "1ccQAGRSCcJbJijorbBzSwU-wx60Ftf-2lzayKzCZQRw"
df = fetch_vendor_data(SHEET_KEY)

# --- Vendor Code Input ---
code_input = st.text_input("Enter your Vendor Code:", value=st.session_state.vendor_code)
st.session_state.vendor_code = code_input

# --- Validate and Process ---
if code_input:
    if "Vendor Code" not in df.columns:
        st.error(" Google Sheet is missing the 'Vendor Code' column.")
        st.stop()

    match = df[df["Vendor Code"] == code_input.upper()]
    if match.empty:
        st.error(" Vendor Code not found.")
        st.stop()

    row = match.iloc[0]
    name = row.get("Name of Vendor", "Vendor")

    try:
        st.markdown(f"###  Report for `{name}`")

        # Score Calculation
        txns = float(row["Monthly Transactions"])
        incomes = [float(row[f"Monthly Income - Month {i}"]) for i in range(1, 4)]
        expenses = [float(row[f"Spending Variance - Month {i}"]) for i in range(1, 4)]
        avg_income = sum(incomes) / 3

        consistency = float(row["Consistency Score"])
        testimonials = float(row["Customer Testimonial"])
        supplier_verified = row["Supplier Verified"]

        credit_score = calculate_credit_score(txns, consistency, supplier_verified, testimonials, txns)
        risk_score = calculate_risk_score(expenses, avg_income)
        risk_level = get_risk_level(risk_score)

        row["Credit Score"] = credit_score
        row["Risk Score"] = risk_score
        row["Risk Level"] = risk_level

        # --- Visualizations ---
        st.subheader(" Credit Score Breakdown (Pie Chart)")
        st.pyplot(draw_vendor_pie_chart(row))

        st.subheader(" Income vs Expense Over Time")
        st.pyplot(draw_vendor_line_chart(row))

        st.subheader(" Credit Factors Bar Chart")
        st.pyplot(draw_vendor_bar_chart(row))

    except Exception as e:
        st.error(f" Error generating chart: {e}")

import streamlit as st
import pandas as pd
from data_fetch import fetch_vendor_data
from calculator import calculate_credit_score, calculate_risk_score, get_risk_level

# --- Page Config ---
st.set_page_config(page_title="Dashboard | SmartSetu-AI", layout="wide")

# --- Load CSS ---
def local_css(path):
    with open(path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("assets/style.css")

# --- Load Header ---
with open("templates/header.html", "r") as f:
    st.markdown(f.read(), unsafe_allow_html=True)

# --- Title ---
st.title("Vendor Dashboard")
st.markdown("View all vendors and individual credit + risk scores")

# --- Fetch Vendor Data ---
SHEET_KEY = "1ccQAGRSCcJbJijorbBzSwU-wx60Ftf-2lzayKzCZQRw"
df = fetch_vendor_data(SHEET_KEY)

if df.empty:
    st.warning("No vendor data found in the Google Sheet.")
    st.stop()

# --- Compute Scores ---
scores = []
max_txn = df["Monthly Transactions"].max()

for index, row in df.iterrows():
    try:
        credit = calculate_credit_score(
            float(row['Monthly Transactions']),
            float(row['Consistency Score']),
            row['Supplier Verified'],
            float(row['Customer Testimonial']),
            max_txn
        )

        income = sum([
            float(row['Monthly Income - Month 1']),
            float(row['Monthly Income - Month 2']),
            float(row['Monthly Income - Month 3'])
        ]) / 3

        expenses = [
            float(row['Spending Variance - Month 1']),
            float(row['Spending Variance - Month 2']),
            float(row['Spending Variance - Month 3'])
        ]

        risk = calculate_risk_score(expenses, income)
        level = get_risk_level(risk)

        scores.append({
            "Vendor": row.get("Name of Vendor", f"Vendor {index+1}"),
            "Credit Score": credit,
            "Risk Score": risk,
            "Risk Level": level
        })

    except Exception as e:
        scores.append({
            "Vendor": row.get("Name of Vendor", f"Vendor {index+1}"),
            "Credit Score": "Error",
            "Risk Score": "Error",
            "Risk Level": f"{type(e).__name__}: {str(e)}"
        })

score_df = pd.DataFrame(scores)

# --- Sidebar ---
st.sidebar.title("Vendor Selector")
selected_vendor = st.sidebar.selectbox("Choose a Vendor:", score_df["Vendor"].tolist())
selected_row = score_df[score_df["Vendor"] == selected_vendor].iloc[0]

st.sidebar.markdown("---")
st.sidebar.markdown("### Vendor Scores")
st.sidebar.metric("Credit Score", selected_row["Credit Score"])
st.sidebar.metric("Risk Score", selected_row["Risk Score"])
st.sidebar.metric("Risk Level", selected_row["Risk Level"])

# --- CSV Download for Selected Vendor ---
vendor_csv = pd.DataFrame([selected_row]).to_csv(index=False).encode("utf-8")
st.sidebar.download_button(
    label="Download Report",
    data=vendor_csv,
    file_name=f"{selected_vendor}_report.csv",
    mime="text/csv"
)

# --- Main Table ---
st.subheader("All Vendor Scores")
st.dataframe(score_df, use_container_width=True)

# --- Full Download ---
st.download_button(
    "Download Full CSV",
    data=score_df.to_csv(index=False).encode("utf-8"),
    file_name="all_vendor_scores.csv",
    mime="text/csv"
)

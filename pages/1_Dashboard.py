import streamlit as st
import pandas as pd
from data_fetch import fetch_vendor_data
from calculator import calculate_credit_score, calculate_risk_score, get_risk_level
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from color_utils import get_score_color, get_level_color


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

# --- Vendor Selection ---
vendor_names = score_df["Vendor"].tolist()
selected_vendor = st.sidebar.selectbox("Select Vendor", vendor_names)
selected_row = score_df[score_df["Vendor"] == selected_vendor].iloc[0]

## --- Sidebar with colored score boxes ---
credit_color = get_score_color(selected_row["Credit Score"], kind="credit")
risk_color = get_score_color(selected_row["Risk Score"], kind="risk")
level_color = get_level_color(selected_row["Risk Level"])

st.sidebar.markdown("---")

#  Uncolored heading
st.sidebar.markdown("<h4 style='font-size:20px; font-weight:700;'> Vendor Scores</h4>", unsafe_allow_html=True)

#  Box for Credit Score
st.sidebar.markdown(f"""
<div style='background-color:#000000; padding:10px 12px; border-radius:10px; margin-bottom:8px;'>
  <span style='font-size:14px;'>Credit Score:</span><br>
  <span style='color:{credit_color}; font-size:18px; font-weight:bold;'>{selected_row["Credit Score"]}</span>
</div>
""", unsafe_allow_html=True)

# Box for Risk Score
st.sidebar.markdown(f"""
<div style='background-color:#000000; padding:10px 12px; border-radius:10px; margin-bottom:8px;'>
  <span style='font-size:14px;'>Risk Score:</span><br>
  <span style='color:{risk_color}; font-size:18px; font-weight:bold;'>{selected_row["Risk Score"]}</span>
</div>
""", unsafe_allow_html=True)

#  Box for Risk Level
st.sidebar.markdown(f"""
<div style='background-color:#000000; padding:10px 12px; border-radius:10px; margin-bottom:8px;'>
  <span style='font-size:14px;'>Risk Level:</span><br>
  <span style='color:{level_color}; font-size:18px; font-weight:bold;'>{selected_row["Risk Level"]}</span>
</div>
""", unsafe_allow_html=True)

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

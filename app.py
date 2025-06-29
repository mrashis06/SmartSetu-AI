import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from data_fetch import fetch_vendor_data
from calculator import calculate_credit_score, calculate_risk_score, get_risk_level

# Google Sheet Key
SHEET_KEY = "1ccQAGRSCcJbJijorbBzSwU-wx60Ftf-2lzayKzCZQRw"
st.set_page_config(page_title="SmartSetu-AI", layout="wide")

# Load custom CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("assets/style.css")

# Load custom header
with open("templates/header.html", "r") as f:
    header_html = f.read()
st.markdown(header_html, unsafe_allow_html=True)

st.title("SmartSetu-AI - Vendor Credit & Risk Scoring Dashboard")

# Fetch vendor data
df = fetch_vendor_data(SHEET_KEY)
if df.empty:
    st.warning("No vendor data found in the connected Google Sheet.")
    st.stop()

# Score calculation
scores = []
max_txn = df["Monthly Transactions"].max()

for index, row in df.iterrows():
    try:
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

        credit_score = calculate_credit_score(transactions, consistency, supplier_verified, testimonials, max_txn)
        risk_score = calculate_risk_score(expenses, avg_income)
        risk_level = get_risk_level(risk_score)

        scores.append({
            "Vendor": row.get("Name of Vendor", f"Vendor {index+1}"),
            "Credit Score": credit_score,
            "Risk Score": risk_score,
            "Risk Level": risk_level
        })

    except Exception as e:
        st.error(f"Error in row {index+1}: {e}")
        scores.append({
            "Vendor": row.get("Name of Vendor", f"Vendor {index+1}"),
            "Credit Score": "Error",
            "Risk Score": "Error",
            "Risk Level": f"{type(e).__name__}: {str(e)}"
        })

# Final DataFrame
score_df = pd.DataFrame(scores)

# --- Sidebar: Vendor Selection ---
st.sidebar.title("Vendor Report Access")

selected_vendor = st.sidebar.selectbox("Choose a Vendor:", score_df["Vendor"].tolist())
selected_row = score_df[score_df["Vendor"] == selected_vendor].iloc[0]

# Display selected vendor scores
st.sidebar.markdown("### Vendor Score Report")
st.sidebar.metric("Credit Score", selected_row["Credit Score"])
st.sidebar.metric("Risk Score", selected_row["Risk Score"])
st.sidebar.metric("Risk Level", selected_row["Risk Level"])

# Download button for selected vendor
vendor_row_df = pd.DataFrame([selected_row])
csv_data = vendor_row_df.to_csv(index=False).encode('utf-8')
st.sidebar.download_button("Download My Report", data=csv_data, file_name=f"{selected_vendor}_report.csv", mime="text/csv")

# --- Main: All Vendors Table ---
st.subheader(" All Vendor Scores")
st.dataframe(score_df, use_container_width=True)

# --- Output Section ---
st.markdown(f"##### Loan Report for **{selected_vendor}**")

st.markdown("### Loan Eligibility & Repayment Details")
credit = selected_row["Credit Score"]
risk = selected_row["Risk Score"]

# Loan Eligibility Logic
if credit >= 80:
    loan_amount = 100000
    interest_rate = 4
elif credit >= 60:
    loan_amount = 50000
    interest_rate = 6
elif credit >= 40:
    loan_amount = 20000
    interest_rate = 8
elif credit >= 30:
    loan_amount = 10000
    interest_rate = 10
else:
    loan_amount = 0
    interest_rate = 0

# EMI Calculator
if loan_amount > 0:
    st.success(f" **Eligible for a loan of ₹{loan_amount:,} at {interest_rate}% interest per year.**")

    st.markdown("###  Simulate Your Loan Repayment")

    # Vendor selects loan amount (within limit)
    custom_loan = st.slider("**Select Loan Amount (₹)**", 1000, loan_amount, step=1000)

    # Vendor selects repayment period
    custom_months = st.slider("**Select Repayment Duration (in months)**", 6, 24, value=12)

    # Calculate total repayment and EMI
    total_repayment = custom_loan + (custom_loan * interest_rate * custom_months / (12 * 100))
    emi = round(total_repayment / custom_months, 2)

    st.markdown(f"""
    -**Loan Amount:** ₹{custom_loan:,}  
    -**Interest Rate:** {interest_rate}%  
    -**Duration:** {custom_months} months  
    -**Monthly EMI:** ₹{emi:,}  
    -**Total Repayment:** ₹{round(total_repayment):,}
    """)

else:
    st.error(" Not eligible for a loan based on current credit score.")

# --- Charts ---
st.subheader(" Visualize Scores")
chart_type = st.selectbox("Select Chart Type:", ["Bar Chart", "Scatter Plot"])
fig_width, fig_height, rotation = (12, 6, 45)

if chart_type == "Bar Chart":
    top_n = st.slider("Select number of vendors", 6, len(score_df), 12, step=2)
    top_df = score_df.sort_values("Credit Score", ascending=False).head(top_n)
    fig, ax = plt.subplots(figsize=(max(10, top_n * 0.6), fig_height))
    x = range(len(top_df))
    bar_width = 0.35
    ax.bar([i - 0.2 for i in x], top_df["Credit Score"], width=bar_width, label="Credit", color="royalblue")
    ax.bar([i + 0.2 for i in x], top_df["Risk Score"], width=bar_width, label="Risk", color="salmon")
    ax.set_xticks(x)
    ax.set_xticklabels(top_df["Vendor"], rotation=rotation)
    ax.legend()
    st.pyplot(fig)

elif chart_type == "Scatter Plot":
    fig, ax = plt.subplots(figsize=(fig_width, fig_height))
    ax.scatter(score_df["Credit Score"], score_df["Risk Score"], c="purple", s=100)
    for i, row in score_df.iterrows():
        ax.text(row["Credit Score"] + 0.5, row["Risk Score"] + 0.5, row["Vendor"], fontsize=8)
    ax.set_xlabel("Credit Score")
    ax.set_ylabel("Risk Score")
    ax.set_title("Credit Score vs Risk Score")
    st.pyplot(fig)

# --- Full CSV ---
st.subheader(" Download All Vendor Scores")
csv_all = score_df.to_csv(index=False).encode('utf-8')
st.download_button("Download Full CSV", csv_all, "vendor_scores.csv", "text/csv")

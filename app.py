import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from data_fetch import fetch_vendor_data
from calculator import calculate_credit_score, calculate_risk_score, get_risk_level
from loan import determine_loan_offer, calculate_emi
from charts import draw_bar_chart, draw_scatter_plot

SHEET_KEY = "1ccQAGRSCcJbJijorbBzSwU-wx60Ftf-2lzayKzCZQRw"
st.set_page_config(page_title="SmartSetu-AI", layout="wide")

# Load custom CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("assets/style.css")

# Load custom header (optional)
with open("templates/header.html", "r") as f:
    header_html = f.read()
st.markdown(header_html, unsafe_allow_html=True)

st.title("SmartSetu-AI - Vendor Credit & Risk Scoring Dashboard")

# --- Fetch vendor data ---
df = fetch_vendor_data(SHEET_KEY)
if df.empty:
    st.warning("No vendor data found in the connected Google Sheet.")
    st.stop()

# --- Calculate scores ---
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
        expenses = [float(row[f'Spending Variance - Month {i}']) for i in range(1, 4)]

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
            "Risk Level": f"{type(e)._name_}: {str(e)}"
        })

score_df = pd.DataFrame(scores)

# --- Sidebar: Vendor Selection ---
st.sidebar.title("Vendor Report Access")
selected_vendor = st.sidebar.selectbox("Choose a Vendor:", score_df["Vendor"].tolist())
selected_row = score_df[score_df["Vendor"] == selected_vendor].iloc[0]
st.sidebar.markdown("### Vendor Score Report")
st.sidebar.metric("Credit Score", selected_row["Credit Score"])
st.sidebar.metric("Risk Score", selected_row["Risk Score"])
st.sidebar.metric("Risk Level", selected_row["Risk Level"])
vendor_row_df = pd.DataFrame([selected_row])
csv_data = vendor_row_df.to_csv(index=False).encode('utf-8')
st.sidebar.download_button("Download My Report", data=csv_data, file_name=f"{selected_vendor}_report.csv", mime="text/csv")

# --- All Vendors Table ---
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader(" All Vendor Scores")
st.dataframe(score_df, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# --- Loan Report ---
st.markdown(f"#####  Loan Report for *{selected_vendor}*")
st.markdown("### Loan Eligibility & Repayment Details")
st.markdown('<div class="card loan-box">', unsafe_allow_html=True)
credit = selected_row["Credit Score"]
loan_amount, interest_rate = determine_loan_offer(credit)
if loan_amount > 0:
    st.success(f" *Eligible for a loan of ₹{loan_amount:,} at {interest_rate}% interest per year.*")
    st.markdown("###  Simulate Your Loan Repayment")
    custom_loan = st.slider("*Select Loan Amount (₹)*", 1000, loan_amount, step=1000)
    custom_months = st.slider("*Select Repayment Duration (in months)*", 6, 24, value=12)
    emi, total_repayment = calculate_emi(custom_loan, custom_months, interest_rate)
    st.markdown(f"""
    -*Loan Amount:* ₹{custom_loan:,}  
    -*Interest Rate:* {interest_rate}%  
    -*Duration:* {custom_months} months  
    -*Monthly EMI:* ₹{emi:,}  
    -*Total Repayment:* ₹{round(total_repayment):,}
    """)
else:
    st.error(" Not eligible for a loan based on current credit score.")
st.markdown('</div>', unsafe_allow_html=True)

# --- Charts ---
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="chart-header"> Visualize Scores</div>', unsafe_allow_html=True)
chart_type = st.selectbox("Select Chart Type:", ["Bar Chart", "Scatter Plot"])
if chart_type == "Bar Chart":
    top_n = st.slider("Select number of vendors", 6, len(score_df), 12, step=2)
    fig = draw_bar_chart(score_df, top_n)
    st.pyplot(fig)
elif chart_type == "Scatter Plot":
    fig = draw_scatter_plot(score_df)
    st.pyplot(fig)
st.markdown('</div>', unsafe_allow_html=True)

# --- Full CSV Download ---
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader(" Download All Vendor Scores")
csv_all = score_df.to_csv(index=False).encode('utf-8')
st.download_button("Download Full CSV", csv_all, "vendor_scores.csv", "text/csv")
st.markdown('</div>', unsafe_allow_html=True)

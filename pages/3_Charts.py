import streamlit as st
from data_fetch import fetch_vendor_data
from charts import draw_bar_chart, draw_scatter_plot, draw_vendor_pie_chart, draw_credit_score_distribution
from calculator import calculate_credit_score, calculate_risk_score, get_risk_level
import pandas as pd

st.set_page_config(page_title="Charts & Visualizations", layout="wide")

with st.container():
    st.title(" SmartSetu-AI Visualizations")

    SHEET_KEY = "1ccQAGRSCcJbJijorbBzSwU-wx60Ftf-2lzayKzCZQRw"
    df = fetch_vendor_data(SHEET_KEY)

    # Calculate scores for all vendors
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
            scores.append({
                "Vendor": row.get("Name of Vendor", f"Vendor {index+1}"),
                "Credit Score": 0,
                "Risk Score": 0,
                "Risk Level": "Error"
            })

    score_df = pd.DataFrame(scores)

    # Section 1: Bar / Scatter Chart
    st.subheader(" Comparative Charts")
    chart_type = st.selectbox("Choose Chart Type:", ["Bar Chart", "Scatter Plot"])
    if chart_type == "Bar Chart":
        top_n = st.slider("Top N Vendors", 6, len(score_df), 12)
        fig = draw_bar_chart(score_df, top_n)
        st.pyplot(fig)
    else:
        fig = draw_scatter_plot(score_df)
        st.pyplot(fig)

    # Section 2: Pie Chart by Vendor
    st.subheader(" Individual Vendor Pie Chart")
    vendor_names = score_df["Vendor"].tolist()
    selected_vendor = st.selectbox("Choose Vendor:", vendor_names)
    vendor_row = score_df[score_df["Vendor"] == selected_vendor].iloc[0]
    fig = draw_vendor_pie_chart(vendor_row)
    st.pyplot(fig)

    # Section 3: Credit Score Distribution Pie Chart
    st.subheader(" Credit Score Category Distribution")
    fig = draw_credit_score_distribution(score_df)
    st.pyplot(fig)

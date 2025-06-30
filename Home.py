import streamlit as st

# --- Page Config ---
st.set_page_config(page_title="SmartSetu-AI", layout="wide")

# --- Load CSS ---
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("assets/style.css")

# --- Load Header ---
with open("templates/header.html", "r") as f:
    st.markdown(f.read(), unsafe_allow_html=True)

# --- Centered Logo & Title ---
st.markdown("""
<div style='text-align: center; margin-top: 30px;'>
    <img src='https://raw.githubusercontent.com/mrashis06/SmartSetu-AI/main/assets/logo.png' class='center-logo'>
    <h1 style='color: white; margin-top: 10px;'>Welcome to SmartSetu-AI</h1>
</div>
""", unsafe_allow_html=True)


# --- Description with Icons ---
st.markdown("""
<div style='text-align: center; font-size: 18px; margin-top: 30px; color: #ccc;'>
    SmartSetu-AI is a financial intelligence tool for assessing vendor creditworthiness and financial risk.
    <br><br>
    <ul style='text-align: left; display: inline-block; list-style: none; padding: 0; font-size: 18px;'>
        <li>📊 <strong>View Vendor Dashboard</strong></li>
        <li>🔍 <strong>Predict Loan Eligibility</strong></li>
        <li>📈 <strong>Visualize Scores</strong></li>
        <li>🏛 <strong>Explore Govt Schemes</strong></li>
    </ul>
</div>
""", unsafe_allow_html=True)

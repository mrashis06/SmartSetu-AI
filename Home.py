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

# --- Centered Logo ---
st.markdown("""
<div style='text-align: center; margin-top: 30px;'>
    <img src='https://raw.githubusercontent.com/mrashis06/SmartSetu-AI/main/assets/logo.png' class='center-logo'>
</div>
""", unsafe_allow_html=True)

# --- Typing Animation ---
st.markdown("""
<style>
@keyframes typing {
  from { width: 0 }
  to { width: 100% }
}
.typing-demo {
  font-family: monospace;
  white-space: nowrap;
  overflow: hidden;
  width: min(90vw, 22ch);
  animation: typing 4s steps(22) forwards;
  font-size: 36px;
  color: white;
  margin: 20px auto 40px auto;
  text-align: center;
}
@media (max-width: 480px) {
  .typing-demo {
    font-size: 24px;
    width: 90vw;
  }
}
</style>
<div class="typing-demo">Welcome to SmartSetu-AI</div>
""", unsafe_allow_html=True)

# --- Main Section with Button ---
# --- Final Section: Features + Button ---
st.markdown("""
<div style='text-align: center; font-size: 18px; margin-top: 30px; color: #ccc; max-width: 800px; margin-left: auto; margin-right: auto; line-height: 1.6;'>
    <strong>SmartSetu-AI</strong> is an innovative financial intelligence platform dedicated to empowering street vendors and small entrepreneurs across India.
    <br><br>
    Our mission is to revolutionize how financial inclusion is achieved by providing smart, data-driven credit assessment and risk analysis — helping vendors unlock easier access to loans and grow their businesses sustainably.
    <br><br>
    Through intuitive dashboards, accurate loan eligibility predictions, and insightful visualizations, we aim to bridge the gap between informal vendors and formal financial systems.
    <br><br>
    Join us on this journey to create a smarter, fairer lending ecosystem — where every hardworking vendor gets the support they deserve.
    <br><br>
    <ul style='text-align: left; display: inline-block; list-style: none; padding: 0; font-size: 18px;'>
        <li>📊 <strong>Explore the Vendor Dashboard</strong> — Real-time financial insights at your fingertips</li>
        <li>🔍 <strong>Predict Loan Eligibility</strong> — AI-powered assessments for accurate credit decisions</li>
        <li>📈 <strong>Visualize Scores</strong> — Easy-to-understand risk and credit metrics</li>
        <li>🏛 <strong>Discover Govt Schemes</strong> — Learn about financial aid and support available</li>
    </ul>
    <br><br>
    <a href="/Vendor_Registration" target="_self" style="
        display: inline-block;
        background-color: #4DC4D2;
        color: black;
        padding: 14px 28px;
        border-radius: 10px;
        font-weight: bold;
        text-decoration: none;
        font-size: 18px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.15);
        transition: 0.3s ease;">
        🚀 Start Predicting
    </a>
</div>
""", unsafe_allow_html=True)


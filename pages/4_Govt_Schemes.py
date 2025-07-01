# 4_Govt_Schemes.py

import sys
import os

# Add the parent directory (root folder) to sys.path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from govt_scheme import get_central_schemes, get_state_scheme
import streamlit as st

st.set_page_config(page_title="Govt Schemes | SmartSetu-AI", layout="wide")

st.title("🏛 Government Financial Schemes for Street Vendors")

# --- CENTRAL SCHEMES ---
st.header("🇮🇳 Central Government Schemes")
central_schemes = get_central_schemes()

for scheme in central_schemes:
    st.subheader(f" {scheme['name']}")
    st.write(scheme["description"])
    st.markdown("**Key Features:**")
    for feature in scheme["features"]:
        st.write(f"- {feature}")
    st.markdown(f"[ Learn More]({scheme['link']})")
    st.markdown("---")

# --- STATE SCHEMES ---
st.header(" State-Wise Financial Support")

state_list = ["Andhra Pradesh", "Madhya Pradesh", "Odisha", "West Bengal", "Bihar", "Uttar Pradesh"]
selected_state = st.selectbox(" Select Your State", state_list)

scheme = get_state_scheme(selected_state)

st.subheader(f" {scheme['state']}")

if scheme["has_own_scheme"]:
    st.write(f"**Scheme Name:** {scheme['scheme_name']}")
else:
    st.warning("This state does not have a separate loan scheme. Central PM SVANidhi is active here.")

st.write(scheme["description"])
if scheme["link"]:
    st.markdown(f"[🔗 More Info]({scheme['link']})")

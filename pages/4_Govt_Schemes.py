import sys
import os
import streamlit as st
from govt_scheme import get_central_schemes, get_state_scheme

# --- Config ---
st.set_page_config(page_title="Govt Schemes | SmartSetu-AI", layout="wide")

# Load CSS and Header
with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
with open("templates/header.html") as f:
    st.markdown(f.read(), unsafe_allow_html=True)

# --- Page Title ---
st.markdown("<h2 style='text-align: center; color: white;'>🏛 Government Financial Schemes for Street Vendors</h2>", unsafe_allow_html=True)

# --- Central Schemes Section ---
with st.container():
    st.markdown("### 🇮🇳 Central Government Schemes")
    central_schemes = get_central_schemes()

    for scheme in central_schemes:
        with st.expander(f" {scheme['name']}"):
            st.write(scheme["description"])
            st.markdown("**Key Features:**")
            for feature in scheme["features"]:
                st.write(f"- {feature}")
            st.markdown(f"[ Learn More]({scheme['link']})", unsafe_allow_html=True)

# --- State Schemes Section ---
with st.container():
    st.markdown("###  State-Wise Financial Support")

    state_list = ["Andhra Pradesh", "Madhya Pradesh", "Odisha", "West Bengal", "Bihar", "Uttar Pradesh"]
    selected_state = st.selectbox(" Select Your State", state_list)

    scheme = get_state_scheme(selected_state)

    with st.container():
        st.markdown(f"<h4 style='color:#4DC4D2;'>{scheme['state']}</h4>", unsafe_allow_html=True)

        if scheme["has_own_scheme"]:
            st.success(f"**Scheme Name:** {scheme['scheme_name']}")
        else:
            st.warning("This state does not have a separate loan scheme. Central PM SVANidhi is active here.")

        st.write(scheme["description"])
        if scheme["link"]:
            st.markdown(f"[ More Info]({scheme['link']})", unsafe_allow_html=True)

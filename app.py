import streamlit as st
from modules.landing import landing_page
from modules.dashboard import dashboard

st.set_page_config(
    page_title="SonicMiner AI",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="collapsed",
)

with open("assets/styles.css", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

if "page" not in st.session_state:
    st.session_state.page = "landing"
if "analyses" not in st.session_state:
    st.session_state.analyses = []

if st.session_state.page == "landing":
    landing_page()
else:
    dashboard()

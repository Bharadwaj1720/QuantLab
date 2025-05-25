import streamlit as st

# MUST BE FIRST Streamlit command
st.set_page_config(page_title="QuantLab Pro", layout="wide")

# THEN import anything else
from app.dashboard import run_dashboard

if __name__ == "__main__":
    run_dashboard()

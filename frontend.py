import streamlit as st
import requests
from pathlib import Path

# ---------------------------------------------------
# Page Configuration
# ---------------------------------------------------

st.set_page_config(
    page_title="Solar Power Forecast Agent",
    page_icon="☀️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------
# Backend Configuration
# ---------------------------------------------------

API_URL = "https://solar-power-forecast-agent.onrender.com"

# ---------------------------------------------------
# Wake Up Backend
# ---------------------------------------------------

try:

    requests.get(
        f"{API_URL}/",
        timeout=30
    )

except requests.exceptions.RequestException:

    # Do not stop the frontend if the backend
    # takes time to wake up.
    pass

# ---------------------------------------------------
# Load Custom CSS
# ---------------------------------------------------

css_file = Path("assets/style.css")

if css_file.exists():

    with open(
        css_file,
        encoding="utf-8"
    ) as f:

        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )

# ---------------------------------------------------
# Sidebar
# ---------------------------------------------------

st.sidebar.image(
    "assets/logo.png",
    width=120
)

st.sidebar.title(
    "Solar Power Forecast Agent"
)

st.sidebar.markdown("---")

st.sidebar.success(
    "Navigation"
)

st.sidebar.info(
    """
    Use the pages in the sidebar to navigate through
    the application.
    """
)

st.sidebar.markdown("---")

st.sidebar.markdown(
    "### Project"
)

st.sidebar.write(
    "Version: 1.0"
)

st.sidebar.write(
    "Model: XGBoost"
)

st.sidebar.write(
    "Framework: Streamlit"
)

# ---------------------------------------------------
# Main Home Screen
# ---------------------------------------------------

st.title(
    "☀ Solar Power Forecast Agent"
)

st.subheader(
    "AI-powered Solar Energy Forecasting and "
    "Recommendation System"
)

st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "Machine Learning Model",
        "XGBoost"
    )

with col2:

    st.metric(
        "Forecast Type",
        "Regression"
    )

with col3:

    st.metric(
        "Weather Features",
        "9"
    )

st.markdown("---")

st.header(
    "Project Overview"
)

st.write(
    """
    This application predicts solar power generation using
    machine learning and weather parameters.

    It also provides

    - Solar Power Forecasting
    - Live Weather Integration
    - AI Energy Assistant
    - Prediction History
    - Analytics Dashboard
    - Report Generation
    - Admin Dashboard
    """
)

st.markdown("---")

st.header(
    "Project Architecture"
)

st.code(
    """
Weather Data
      │
      ▼
Data Preprocessing
      │
      ▼
Feature Engineering
      │
      ▼
XGBoost Prediction Model
      │
      ▼
AI Recommendation Engine
      │
      ▼
Dashboard & Reports
"""
)

st.markdown("---")

st.info(
    """
    👈 Use the sidebar to access:

    • Solar Forecast

    • Live Weather

    • AI Energy Assistant

    • History

    • Analytics

    • Admin Dashboard

    • Settings
    """
)

st.markdown("---")

st.caption(
    "© 2026 Solar Power Forecast Agent | "
    "Built with Python, Streamlit, FastAPI and XGBoost"
)

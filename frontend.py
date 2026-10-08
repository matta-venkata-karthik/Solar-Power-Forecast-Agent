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

# ==========================================================
# Backend Connection
# ==========================================================

def check_backend_connection():
    """
    Check and wake the FastAPI backend.

    The frontend automatically calls the backend health
    endpoint when the Streamlit session starts.

    The function makes several attempts because Render may
    need some time to wake a sleeping service.
    """

    # Do not repeatedly wake the backend on every Streamlit
    # rerun during the same browser session.
    if st.session_state.get(
        "backend_checked",
        False,
    ):

        return st.session_state.get(
            "backend_available",
            False,
        )

    st.session_state[
        "backend_checked"
    ] = True

    st.session_state[
        "backend_available"
    ] = False

    max_attempts = 4

    for attempt in range(
        1,
        max_attempts + 1,
    ):

        try:

            result = health_check()

            # Support either:
            # True
            # {"status": "healthy"}
            # {"status": "ok"}
            if result is True:

                st.session_state[
                    "backend_available"
                ] = True

                return True

            if isinstance(
                result,
                dict,
            ):

                status = str(
                    result.get(
                        "status",
                        "",
                    )
                ).lower()

                if status in {
                    "healthy",
                    "ok",
                    "online",
                    "running",
                    "success",
                }:

                    st.session_state[
                        "backend_available"
                    ] = True

                    return True

        except Exception:
            pass

        # Give Render time to wake up before trying again.
        if attempt < max_attempts:

            time.sleep(
                attempt * 2
            )

    return False


# ==========================================================
# Start Backend Connection
# ==========================================================

with st.spinner(
    "🔄 Connecting to backend...
    It May Take a Minute"
):

    backend_available = (
        check_backend_connection()
    )

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

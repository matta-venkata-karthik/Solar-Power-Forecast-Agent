import time
from pathlib import Path

import requests
import streamlit as st


# ==========================================================
# Configuration
# ==========================================================

API_URL = "https://solar-power-forecast-agent.onrender.com"

# ==========================================================
# Page Configuration
# ==========================================================

st.set_page_config(
    page_title="Solar Power Forecast Agent",
    page_icon="☀️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==========================================================
# Backend Functions
# ==========================================================

def get_api_url():
    """
    Return the deployed FastAPI backend URL.
    """
    return API_URL


def health_check():
    """
    Check whether the FastAPI backend is available.
    """

    response = requests.get(
        f"{API_URL}/health",
        timeout=20
    )

    response.raise_for_status()

    return response.json()


def check_backend_connection():
    """
    Check and wake the FastAPI backend.

    The frontend automatically calls the backend
    health endpoint when the Streamlit session starts.

    Render may need some time to wake a sleeping service,
    so multiple attempts are performed.
    """

    # ------------------------------------------------------
    # Avoid checking repeatedly during the same session
    # ------------------------------------------------------

    if st.session_state.get(
        "backend_checked",
        False
    ):

        return st.session_state.get(
            "backend_available",
            False
        )

    # ------------------------------------------------------
    # Initialize connection state
    # ------------------------------------------------------

    st.session_state[
        "backend_checked"
    ] = True

    st.session_state[
        "backend_available"
    ] = False

    # ------------------------------------------------------
    # Connection attempts
    # ------------------------------------------------------

    max_attempts = 4

    for attempt in range(
        1,
        max_attempts + 1
    ):

        try:

            result = health_check()

            # ------------------------------------------------
            # Support simple True response
            # ------------------------------------------------

            if result is True:

                st.session_state[
                    "backend_available"
                ] = True

                return True

            # ------------------------------------------------
            # Support JSON health response
            # ------------------------------------------------

            if isinstance(
                result,
                dict
            ):

                status = str(
                    result.get(
                        "status",
                        ""
                    )
                ).lower()

                if status in {
                    "healthy",
                    "ok",
                    "online",
                    "running",
                    "success"
                }:

                    st.session_state[
                        "backend_available"
                    ] = True

                    return True

        except Exception:

            pass

        # ----------------------------------------------------
        # Wait before retrying
        # ----------------------------------------------------

        if attempt < max_attempts:

            time.sleep(
                attempt * 2
            )

    return False


# ==========================================================
# Load Custom CSS
# ==========================================================

css_file = Path(
    "assets/style.css"
)

if css_file.exists():

    with open(
        css_file,
        encoding="utf-8"
    ) as f:

        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )


# ==========================================================
# Start Backend Connection
# ==========================================================

with st.spinner(
    "🔄 Connecting to backend... It May Take a Minute"
):

    backend_available = (
        check_backend_connection()
    )


# ==========================================================
# Sidebar
# ==========================================================

with st.sidebar:

    # ------------------------------------------------------
    # Logo
    # ------------------------------------------------------

    logo = Path(
        "assets/logo.png"
    )

    if logo.exists():

        st.image(
            str(logo),
            width=120
        )

    st.title(
        "Solar Power Forecast Agent"
    )

    st.markdown("---")

    # ------------------------------------------------------
    # Backend Status
    # ------------------------------------------------------

    if backend_available:

        st.success(
            "🟢 Backend Connected"
        )

        st.caption(
            API_URL
        )

    else:

        st.error(
            "🔴 Backend Unavailable"
        )

        st.caption(
            API_URL
        )

        if st.button(
            "🔄 Retry Backend",
            use_container_width=True
        ):

            st.session_state[
                "backend_checked"
            ] = False

            st.session_state[
                "backend_available"
            ] = False

            st.rerun()

    st.markdown("---")

    # ------------------------------------------------------
    # Navigation
    # ------------------------------------------------------

    st.success(
        "Navigation"
    )

    st.info(
        """
        Use the pages in the sidebar to navigate
        through the application.
        """
    )

    st.markdown("---")

    # ------------------------------------------------------
    # Project Information
    # ------------------------------------------------------

    st.markdown(
        "### Project"
    )

    st.write(
        "Version: 1.0"
    )

    st.write(
        "Model: XGBoost"
    )

    st.write(
        "Framework: Streamlit"
    )


# ==========================================================
# Main Home Screen
# ==========================================================

st.title(
    "☀ Solar Power Forecast Agent"
)

st.subheader(
    "AI-powered Solar Energy Forecasting and "
    "Recommendation System"
)

st.markdown("---")


# ==========================================================
# Model Information
# ==========================================================

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


# ==========================================================
# Project Overview
# ==========================================================

st.header(
    "Project Overview"
)

st.write(
    """
    This application predicts solar power generation using
    machine learning and weather parameters.

    It also provides:

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


# ==========================================================
# Backend Information
# ==========================================================

st.header(
    "Backend Status"
)

if backend_available:

    st.success(
        "🟢 FastAPI backend is connected and ready."
    )

else:

    st.error(
        """
        🔴 The FastAPI backend is currently unavailable.

        The frontend will remain available, but prediction
        and other backend-dependent features may not work
        until the backend becomes available.
        """
    )


st.markdown("---")


# ==========================================================
# Project Architecture
# ==========================================================

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


# ==========================================================
# Navigation Information
# ==========================================================

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


# ==========================================================
# Footer
# ==========================================================

st.caption(
    "© 2026 Solar Power Forecast Agent | "
    "Built with Python, Streamlit, FastAPI and XGBoost"
)

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
    Check the FastAPI backend health endpoint.
    """

    response = requests.get(
        f"{API_URL}/health",
        timeout=10
    )

    response.raise_for_status()

    return response.json()


def backend_is_healthy(result):
    """
    Check supported health-check responses.
    """

    if result is True:
        return True

    if isinstance(result, dict):

        status = str(
            result.get(
                "status",
                ""
            )
        ).lower()

        return status in {
            "healthy",
            "ok",
            "online",
            "running",
            "success"
        }

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
# Session State
# ==========================================================

if "backend_available" not in st.session_state:

    st.session_state[
        "backend_available"
    ] = False


if "backend_attempts" not in st.session_state:

    st.session_state[
        "backend_attempts"
    ] = 0


if "backend_checked" not in st.session_state:

    st.session_state[
        "backend_checked"
    ] = False


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

    else:

        st.markdown(
            """
            <div style="
                text-align:center;
                font-size:42px;
                padding:10px;
            ">
                ☀️
            </div>
            """,
            unsafe_allow_html=True
        )

    # ------------------------------------------------------
    # Project Title
    # ------------------------------------------------------

    st.title(
        "Solar Power Forecast Agent"
    )

    st.markdown(
        """
        <div style="
            font-size:13px;
            opacity:0.7;
            margin-bottom:10px;
        ">
            AI-powered solar forecasting platform
        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    # ------------------------------------------------------
    # Backend Status Placeholder
    # ------------------------------------------------------

    backend_status_placeholder = st.empty()

    backend_url_placeholder = st.empty()

    st.divider()

    # ------------------------------------------------------
    # Quick Navigation
    # ------------------------------------------------------

    st.markdown(
        "### 🧭 Quick Navigation"
    )

    st.caption(
        "Use the navigation menu to open the "
        "different sections of the application."
    )

    st.divider()

    # ------------------------------------------------------
    # Project Information
    # ------------------------------------------------------

    st.markdown(
        "### Project"
    )

    st.caption(
        "Version: 1.0"
    )

    st.caption(
        "Model: XGBoost"
    )

    st.caption(
        "Framework: Streamlit"
    )


# ==========================================================
# Backend Connection Fragment
# ==========================================================

@st.fragment(run_every="2s")
def backend_connection():

    # ------------------------------------------------------
    # Already connected
    # ------------------------------------------------------

    if st.session_state.get(
        "backend_available",
        False
    ):

        backend_status_placeholder.success(
            "🟢 Backend Connected"
        )

        backend_url_placeholder.caption(
            f"Backend: {API_URL}"
        )

        return

    # ------------------------------------------------------
    # Maximum startup attempts
    # ------------------------------------------------------

    max_attempts = 4

    attempts = st.session_state.get(
        "backend_attempts",
        0
    )

    # ------------------------------------------------------
    # Backend unavailable after attempts
    # ------------------------------------------------------

    if attempts >= max_attempts:

        backend_status_placeholder.error(
            "🔴 Backend Unavailable"
        )

        backend_url_placeholder.caption(
            f"Backend: {API_URL}"
        )

        if st.button(
            "🔄 Retry Backend",
            use_container_width=True,
            key="retry_backend"
        ):

            st.session_state[
                "backend_attempts"
            ] = 0

            st.session_state[
                "backend_checked"
            ] = False

            st.session_state[
                "backend_available"
            ] = False

            st.rerun()

        return

    # ------------------------------------------------------
    # Show connecting status
    # ------------------------------------------------------

    backend_status_placeholder.info(
        "🔄 Connecting to backend..."
    )

    backend_url_placeholder.caption(
        f"Backend: {API_URL}"
    )

    # ------------------------------------------------------
    # Try backend
    # ------------------------------------------------------

    try:

        result = health_check()

        if backend_is_healthy(result):

            st.session_state[
                "backend_available"
            ] = True

            st.session_state[
                "backend_checked"
            ] = True

            backend_status_placeholder.success(
                "🟢 Backend Connected"
            )

            backend_url_placeholder.caption(
                f"Backend: {API_URL}"
            )

            return

    except requests.exceptions.Timeout:

        pass

    except requests.exceptions.ConnectionError:

        pass

    except requests.exceptions.RequestException:

        pass

    except Exception:

        pass

    # ------------------------------------------------------
    # Failed attempt
    # ------------------------------------------------------

    st.session_state[
        "backend_attempts"
    ] = attempts + 1


# ==========================================================
# Start Backend Connection
# ==========================================================

backend_connection()


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

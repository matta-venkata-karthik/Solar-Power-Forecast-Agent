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
# Load Custom CSS
# ==========================================================

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


# ==========================================================
# Session State
# ==========================================================

if "backend_available" not in st.session_state:

    st.session_state[
        "backend_available"
    ] = False


if "backend_checked" not in st.session_state:

    st.session_state[
        "backend_checked"
    ] = False


if "backend_attempts" not in st.session_state:

    st.session_state[
        "backend_attempts"
    ] = 0


# ==========================================================
# Backend Functions
# ==========================================================

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


def is_backend_healthy(data):
    """
    Validate the FastAPI health response.
    """

    if data is True:
        return True

    if isinstance(data, dict):

        status = str(
            data.get(
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


def check_backend():
    """
    Try to connect to the FastAPI backend.

    Render may need time to wake up, so the
    frontend makes several attempts.
    """

    max_attempts = 4

    current_attempt = st.session_state.get(
        "backend_attempts",
        0
    )

    if current_attempt >= max_attempts:

        return False

    try:

        result = health_check()

        if is_backend_healthy(result):

            st.session_state[
                "backend_available"
            ] = True

            st.session_state[
                "backend_checked"
            ] = True

            return True

    except (
        requests.exceptions.Timeout,
        requests.exceptions.ConnectionError,
        requests.exceptions.RequestException
    ):

        pass

    except Exception:

        pass

    st.session_state[
        "backend_attempts"
    ] = current_attempt + 1

    return False


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
    # Backend Status
    # ------------------------------------------------------

    if st.session_state.get(
        "backend_available",
        False
    ):

        st.success(
            "🟢 Backend Connected"
        )

    else:

        st.info(
            "🔄 Connecting to backend..."
        )

    st.caption(
        f"Backend: {API_URL}"
    )

    # ------------------------------------------------------
    # Retry Button
    # ------------------------------------------------------

    if not st.session_state.get(
        "backend_available",
        False
    ):

        if st.session_state.get(
            "backend_attempts",
            0
        ) >= 4:

            if st.button(
                "🔄 Retry Backend",
                use_container_width=True
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
# Backend Connection
# ==========================================================

if not st.session_state.get(
    "backend_available",
    False
):

    if not st.session_state.get(
        "backend_checked",
        False
    ):

        # --------------------------------------------------
        # Try backend connection
        # --------------------------------------------------

        backend_connected = check_backend()

        if backend_connected:

            st.session_state[
                "backend_checked"
            ] = True

            st.rerun()

        else:

            # ------------------------------------------------
            # Allow the page to render first.
            # The next Streamlit rerun will try again.
            # ------------------------------------------------

            if st.session_state.get(
                "backend_attempts",
                0
            ) < 4:

                time.sleep(0.2)

                st.rerun()

            else:

                st.session_state[
                    "backend_checked"
                ] = True


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

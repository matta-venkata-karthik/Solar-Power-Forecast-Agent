# ==========================================================
# SOLAR POWER FORECAST AGENT
# Main Streamlit Application
# ==========================================================

import time
from pathlib import Path

import requests
import streamlit as st


# ==========================================================
# Project Paths
# ==========================================================

FRONTEND_DIR = Path(
    __file__
).resolve().parent

ASSETS_DIR = (
    FRONTEND_DIR
    / "assets"
)

CSS_PATH = (
    ASSETS_DIR
    / "style.css"
)

LOGO_PATH = (
    ASSETS_DIR
    / "logo.png"
)


# ==========================================================
# Backend Configuration
# ==========================================================

API_URL = (
    "https://solar-power-forecast-agent.onrender.com"
)


# ==========================================================
# Page Configuration
# ==========================================================

st.set_page_config(
    page_title="Solar Power Forecast Agent",
    page_icon="☀️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ==========================================================
# Load Custom CSS
# ==========================================================

if CSS_PATH.exists():

    try:

        with open(
            CSS_PATH,
            encoding="utf-8",
        ) as f:

            st.markdown(
                f"<style>{f.read()}</style>",
                unsafe_allow_html=True,
            )

    except Exception:
        pass


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

    The function first tries /health. If the backend does
    not expose /health, it falls back to the root endpoint.
    """

    # ------------------------------------------------------
    # Try /health first
    # ------------------------------------------------------

    try:

        response = requests.get(
            f"{API_URL}/health",
            timeout=15,
        )

        if response.status_code == 200:

            return response

    except (
        requests.exceptions.Timeout,
        requests.exceptions.ConnectionError,
        requests.exceptions.RequestException,
    ):

        pass

    # ------------------------------------------------------
    # Fallback to root endpoint
    # ------------------------------------------------------

    try:

        response = requests.get(
            API_URL,
            timeout=15,
        )

        if response.status_code == 200:

            return response

    except (
        requests.exceptions.Timeout,
        requests.exceptions.ConnectionError,
        requests.exceptions.RequestException,
    ):

        pass

    return None


def backend_is_healthy(
    response,
):
    """
    Determine whether the backend response indicates
    a healthy/running FastAPI service.
    """

    if response is None:

        return False

    if response.status_code != 200:

        return False

    # ------------------------------------------------------
    # Try JSON health response
    # ------------------------------------------------------

    try:

        data = response.json()

        if isinstance(
            data,
            dict,
        ):

            status = str(
                data.get(
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

                return True

            # A valid JSON response from the backend is
            # also considered a successful connection.
            return True

    except Exception:

        pass

    # ------------------------------------------------------
    # HTTP 200 is sufficient for root endpoint
    # ------------------------------------------------------

    return True


# ==========================================================
# Backend Connection
# ==========================================================

def connect_to_backend():
    """
    Automatically connect to the Render backend.

    Render may put the service to sleep after inactivity.
    Several attempts are made automatically to give Render
    time to wake the FastAPI application.
    """

    # ------------------------------------------------------
    # Already connected
    # ------------------------------------------------------

    if st.session_state.get(
        "backend_available",
        False,
    ):

        return True


    # ------------------------------------------------------
    # Already checked
    # ------------------------------------------------------

    if st.session_state.get(
        "backend_checked",
        False,
    ):

        return False


    # ------------------------------------------------------
    # Reset connection state
    # ------------------------------------------------------

    st.session_state[
        "backend_available"
    ] = False

    st.session_state[
        "backend_attempts"
    ] = 0


    max_attempts = 4


    # ------------------------------------------------------
    # Connection attempts
    # ------------------------------------------------------

    for attempt in range(
        1,
        max_attempts + 1,
    ):

        st.session_state[
            "backend_attempts"
        ] = attempt


        response = health_check()


        if backend_is_healthy(
            response
        ):

            st.session_state[
                "backend_available"
            ] = True

            st.session_state[
                "backend_checked"
            ] = True

            return True


        # --------------------------------------------------
        # Wait for Render cold start
        # --------------------------------------------------

        if attempt < max_attempts:

            time.sleep(
                attempt * 2
            )


    # ------------------------------------------------------
    # Backend unavailable
    # ------------------------------------------------------

    st.session_state[
        "backend_available"
    ] = False

    st.session_state[
        "backend_checked"
    ] = True

    return False


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
# Backend Startup Connection
# ==========================================================

if not st.session_state.get(
    "backend_checked",
    False,
):

    with st.spinner(
        "🔄 Connecting to Solar Power Forecast backend..."
    ):

        backend_available = (
            connect_to_backend()
        )

else:

    backend_available = (
        st.session_state.get(
            "backend_available",
            False,
        )
    )


# ==========================================================
# Sidebar
# ==========================================================

with st.sidebar:

    # ------------------------------------------------------
    # Logo
    # ------------------------------------------------------

    if LOGO_PATH.exists():

        st.image(
            str(LOGO_PATH),
            width=120,
        )

    else:

        st.markdown(
            """
            <div style="
                text-align:center;
                font-size:48px;
                padding:10px;
            ">
                ☀️
            </div>
            """,
            unsafe_allow_html=True,
        )


    # ------------------------------------------------------
    # Project Title
    # ------------------------------------------------------

    st.markdown(
        """
        <div style="
            font-size:23px;
            font-weight:700;
            line-height:1.2;
            margin-top:12px;
            margin-bottom:18px;
        ">
            Solar Power Forecast Agent
        </div>
        """,
        unsafe_allow_html=True,
    )


    st.divider()


    # ======================================================
    # BACKEND STATUS
    # ======================================================

    if backend_available:

        st.success(
            "🟢 Backend Connected"
        )

    else:

        st.error(
            "🔴 Backend Unavailable"
        )


    # ------------------------------------------------------
    # Backend URL
    # ------------------------------------------------------

    st.caption(
        f"Backend: {get_api_url()}"
    )


    # ------------------------------------------------------
    # Retry Backend
    # ------------------------------------------------------

    if not backend_available:

        if st.button(
            "🔄 Retry Backend",
            use_container_width=True,
            key="sidebar_retry_backend",
        ):

            st.session_state[
                "backend_checked"
            ] = False

            st.session_state[
                "backend_available"
            ] = False

            st.session_state[
                "backend_attempts"
            ] = 0

            st.rerun()


    st.divider()


    # ------------------------------------------------------
    # Navigation Information
    # ------------------------------------------------------

    st.markdown(
        """
        <div style="
            font-weight:700;
            font-size:18px;
            margin-bottom:10px;
        ">
            🧭 Navigation
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.info(
        "Use the pages in the sidebar to navigate "
        "through the application."
    )


    st.divider()


    # ------------------------------------------------------
    # Project Information
    # ------------------------------------------------------

    st.markdown(
        """
        <div style="
            font-weight:700;
            font-size:18px;
            margin-bottom:10px;
        ">
            Project
        </div>
        """,
        unsafe_allow_html=True,
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
# Main Page
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
# Backend Main Status
# ==========================================================

if backend_available:

    st.success(
        "🟢 Backend is connected. "
        "The application is ready to use."
    )

else:

    st.warning(
        """
        🟡 The frontend is running, but the FastAPI
        backend is currently unavailable.

        Render may still be waking the backend.

        Please use **Retry Backend** from the sidebar
        after a short wait.
        """
    )


# ==========================================================
# Model Information
# ==========================================================

col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "Machine Learning Model",
        "XGBoost",
    )


with col2:

    st.metric(
        "Forecast Type",
        "Regression",
    )


with col3:

    st.metric(
        "Weather Features",
        "9",
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
"""
)

st.write(
    "It also provides:"
)

st.markdown(
    """
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

st.header(
    "Application Navigation"
)

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
# Application Status
# ==========================================================

st.header(
    "💻 Application Status"
)

status_col1, status_col2 = st.columns(2)


with status_col1:

    if backend_available:

        st.success(
            "🟢 Backend Connected"
        )

    else:

        st.error(
            "🔴 Backend Unavailable"
        )


with status_col2:

    st.info(
        f"Backend: {get_api_url()}"
    )


st.markdown("---")


# ==========================================================
# System Information
# ==========================================================

st.header(
    "System Information"
)

info1, info2, info3, info4 = st.columns(4)


with info1:

    st.metric(
        "Backend",
        "FastAPI",
    )


with info2:

    st.metric(
        "Frontend",
        "Streamlit",
    )


with info3:

    st.metric(
        "Machine Learning",
        "XGBoost",
    )


with info4:

    st.metric(
        "Weather Features",
        "9",
    )


st.markdown("---")


# ==========================================================
# Backend Information
# ==========================================================

st.subheader(
    "🔗 Backend Connection"
)

st.code(
    get_api_url()
)


if backend_available:

    st.success(
        "✅ FastAPI backend is online and responding."
    )

else:

    st.warning(
        "⚠️ FastAPI backend is not responding yet."
    )


st.markdown("---")


# ==========================================================
# Footer
# ==========================================================

st.caption(
    "© 2026 Solar Power Forecast Agent | "
    "Built with Python, Streamlit, FastAPI and XGBoost"
)

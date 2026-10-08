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
    initial_sidebar_state="expanded",
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
        timeout=15,
    )

    response.raise_for_status()

    return response.json()


def backend_is_healthy(result):
    """
    Check supported health-check responses.
    """

    if result is True:
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

        return status in {
            "healthy",
            "ok",
            "online",
            "running",
            "success",
        }

    return False


# ==========================================================
# Load Custom CSS
# ==========================================================

css_file = Path(
    "assets/style.css"
)

if css_file.exists():

    try:

        with open(
            css_file,
            encoding="utf-8",
        ) as f:

            st.markdown(
                f"<style>{f.read()}</style>",
                unsafe_allow_html=True,
            )

    except Exception:
        pass


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
# Backend Connection
# ==========================================================

def connect_to_backend():
    """
    Automatically connect to the FastAPI backend.

    This is called when the Streamlit frontend starts.

    Render services can take some time to wake up after
    inactivity, so several attempts are made automatically.
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
    # Already checked and failed
    # ------------------------------------------------------

    if st.session_state.get(
        "backend_checked",
        False,
    ):

        return False


    max_attempts = 4

    for attempt in range(
        1,
        max_attempts + 1,
    ):

        st.session_state[
            "backend_attempts"
        ] = attempt


        try:

            result = health_check()

            if backend_is_healthy(
                result
            ):

                st.session_state[
                    "backend_available"
                ] = True

                st.session_state[
                    "backend_checked"
                ] = True

                return True


        except requests.exceptions.Timeout:

            pass

        except requests.exceptions.ConnectionError:

            pass

        except requests.exceptions.RequestException:

            pass

        except Exception:

            pass


        # --------------------------------------------------
        # Wait before next attempt.
        #
        # Render may be waking the backend.
        # --------------------------------------------------

        if attempt < max_attempts:

            time.sleep(
                attempt * 2
            )


    # ------------------------------------------------------
    # All attempts failed
    # ------------------------------------------------------

    st.session_state[
        "backend_available"
    ] = False

    st.session_state[
        "backend_checked"
    ] = True

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
            width=120,
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
            unsafe_allow_html=True,
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
        unsafe_allow_html=True,
    )


    st.divider()


    # ------------------------------------------------------
    # Backend Connection Status
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
# Start Backend Connection
# ==========================================================

if not st.session_state.get(
    "backend_checked",
    False,
):

    backend_status_placeholder.info(
        "🔄 Connecting to backend..."
    )

    backend_url_placeholder.caption(
        f"Backend: {API_URL}"
    )

    with st.spinner(
        "Waking up Solar Power Forecast backend..."
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
# Update Sidebar Backend Status
# ==========================================================

if backend_available:

    backend_status_placeholder.success(
        "🟢 Backend Connected"
    )

    backend_url_placeholder.caption(
        f"Backend: {API_URL}"
    )

else:

    backend_status_placeholder.error(
        "🔴 Backend Unavailable"
    )

    backend_url_placeholder.caption(
        f"Backend: {API_URL}"
    )

    if st.button(
        "🔄 Retry Backend",
        use_container_width=True,
        key="retry_backend",
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
# Backend Connection Message
# ==========================================================

if backend_available:

    st.success(
        "🟢 Solar Power Forecast backend is connected."
    )

else:

    st.warning(
        """
        ⚠️ The Solar Power Forecast backend is currently
        unavailable.

        Please use **Retry Backend** in the sidebar.
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
# Backend Status
# ==========================================================

st.header(
    "Backend Status"
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
        f"Backend: {API_URL}"
    )


st.markdown("---")


# ==========================================================
# Footer
# ==========================================================

st.caption(
    "© 2026 Solar Power Forecast Agent | "
    "Built with Python, Streamlit, FastAPI and XGBoost"
)

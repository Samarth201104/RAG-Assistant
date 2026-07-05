"""
File: frontend/utils/session.py

Session State Manager
"""

from __future__ import annotations

from datetime import datetime

import streamlit as st

from utils.constants import DEFAULT_PAGE


# =============================================================================
# Session Initialization
# =============================================================================

def initialize_session() -> None:
    """
    Initialize Streamlit session state.
    Safe to call multiple times.
    """

    defaults = {

        # Navigation
        "current_page": DEFAULT_PAGE,

        # Chat
        "chat_history": [],

        # Upload
        "uploaded_files": [],

        # Dashboard
        "backend_status": "Offline",
        "document_count": 0,
        "chunk_count": 0,

        # Processing
        "is_processing": False,

        # Notifications
        "success_message": "",
        "error_message": "",
        "warning_message": "",

        # Current Results
        "summary": None,
        "comparison": None,
        "notes": None,

        # Startup
        "startup_time": datetime.now(),

    }

    for key, value in defaults.items():

        if key not in st.session_state:

            st.session_state[key] = value


# =============================================================================
# Navigation
# =============================================================================

def get_current_page() -> str:
    """
    Return current page.
    """

    return st.session_state.current_page


def set_current_page(
    page: str,
) -> None:
    """
    Update current page.
    """

    st.session_state.current_page = page


# =============================================================================
# Dashboard
# =============================================================================

def update_dashboard(
    backend_status: str,
    document_count: int,
    chunk_count: int,
) -> None:
    """
    Update dashboard statistics.
    """

    st.session_state.backend_status = backend_status
    st.session_state.document_count = document_count
    st.session_state.chunk_count = chunk_count


# =============================================================================
# Chat
# =============================================================================

def add_chat_message(
    role: str,
    message: str,
    citations: list | None = None,
) -> None:
    """
    Add message to chat history.
    """

    st.session_state.chat_history.append(
        {

            "role": role,

            "message": message,

            "citations": citations or [],

            "timestamp": datetime.now(),

        }
    )


def get_chat_history() -> list:
    """
    Return chat history.
    """

    return st.session_state.chat_history


def clear_chat() -> None:
    """
    Clear conversation.
    """

    st.session_state.chat_history = []


# =============================================================================
# Upload
# =============================================================================

def set_uploaded_files(
    files: list,
) -> None:
    """
    Store uploaded files.
    """

    st.session_state.uploaded_files = files


def get_uploaded_files() -> list:
    """
    Return uploaded files.
    """

    return st.session_state.uploaded_files


# =============================================================================
# Processing
# =============================================================================

def set_processing(
    value: bool,
) -> None:
    """
    Set processing state.
    """

    st.session_state.is_processing = value


def is_processing() -> bool:
    """
    Return processing state.
    """

    return st.session_state.is_processing


# =============================================================================
# Notifications
# =============================================================================

def set_success(
    message: str,
) -> None:
    """
    Store success message.
    """

    st.session_state.success_message = message


def set_error(
    message: str,
) -> None:
    """
    Store error message.
    """

    st.session_state.error_message = message


def set_warning(
    message: str,
) -> None:
    """
    Store warning message.
    """

    st.session_state.warning_message = message


def clear_notifications() -> None:
    """
    Remove all notifications.
    """

    st.session_state.success_message = ""
    st.session_state.error_message = ""
    st.session_state.warning_message = ""


# =============================================================================
# Results
# =============================================================================

def set_summary(
    summary,
) -> None:

    st.session_state.summary = summary


def get_summary():

    return st.session_state.summary


def set_comparison(
    comparison,
) -> None:

    st.session_state.comparison = comparison


def get_comparison():

    return st.session_state.comparison


def set_notes(
    notes,
) -> None:

    st.session_state.notes = notes


def get_notes():

    return st.session_state.notes


# =============================================================================
# Session Information
# =============================================================================

def session_duration() -> str:
    """
    Return current session duration.
    """

    delta = datetime.now() - st.session_state.startup_time

    minutes = int(delta.total_seconds() // 60)

    hours = minutes // 60

    minutes %= 60

    if hours:

        return f"{hours}h {minutes}m"

    return f"{minutes}m"
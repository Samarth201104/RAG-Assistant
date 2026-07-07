"""
File: frontend/utils/session.py

Enterprise Session State Manager
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

        # ---------------------------------------------------------------------
        # Navigation
        # ---------------------------------------------------------------------

        "current_page": DEFAULT_PAGE,

        # ---------------------------------------------------------------------
        # Chat
        # ---------------------------------------------------------------------

        "chat_history": [],

        # ---------------------------------------------------------------------
        # Upload
        # ---------------------------------------------------------------------

        "uploaded_files": [],

        # ---------------------------------------------------------------------
        # Dashboard
        # ---------------------------------------------------------------------

        "backend_status": "Offline",

        "document_count": 0,

        "chunk_count": 0,

        # ---------------------------------------------------------------------
        # Processing
        # ---------------------------------------------------------------------

        "is_processing": False,

        # ---------------------------------------------------------------------
        # Notifications
        # ---------------------------------------------------------------------

        "success_message": "",

        "error_message": "",

        "warning_message": "",

        # ---------------------------------------------------------------------
        # Generated Results
        # ---------------------------------------------------------------------

        "summary": None,

        "comparison": None,

        "notes": None,

        # ---------------------------------------------------------------------
        # Startup
        # ---------------------------------------------------------------------

        "startup_complete": False,

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
    Update dashboard metrics.
    """

    st.session_state.backend_status = backend_status

    st.session_state.document_count = document_count

    st.session_state.chunk_count = chunk_count


def update_statistics(
    document_count: int,
    chunk_count: int,
) -> None:
    """
    Backward compatible helper.
    """

    st.session_state.document_count = document_count

    st.session_state.chunk_count = chunk_count


# =============================================================================
# Chat
# =============================================================================

def add_chat_message(
    role: str,
    content: str,
    citations: list | None = None,
) -> None:
    """
    Append one message to chat history.
    """

    st.session_state.chat_history.append(

        {

            "role": role,

            "content": content,

            "citations": citations or [],

            "timestamp": datetime.now(),

        }

    )


def get_chat_history() -> list:
    """
    Return chat history.
    """

    return st.session_state.chat_history


def set_chat_history(
    history: list,
) -> None:
    """
    Replace complete chat history.
    """

    st.session_state.chat_history = history


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
    Update processing state.
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


def get_success() -> str:
    """
    Return success message.
    """

    return st.session_state.success_message


def set_error(
    message: str,
) -> None:
    """
    Store error message.
    """

    st.session_state.error_message = message


def get_error() -> str:
    """
    Return error message.
    """

    return st.session_state.error_message


def set_warning(
    message: str,
) -> None:
    """
    Store warning message.
    """

    st.session_state.warning_message = message


def get_warning() -> str:
    """
    Return warning message.
    """

    return st.session_state.warning_message


def clear_notifications() -> None:
    """
    Clear all notification messages.
    """

    st.session_state.success_message = ""

    st.session_state.error_message = ""

    st.session_state.warning_message = ""


# =============================================================================
# Summary
# =============================================================================

def set_summary(
    summary,
) -> None:
    """
    Store generated summary.
    """

    st.session_state.summary = summary


def get_summary():
    """
    Return generated summary.
    """

    return st.session_state.summary


def clear_summary() -> None:
    """
    Remove generated summary.
    """

    st.session_state.summary = None


# =============================================================================
# Comparison
# =============================================================================

def set_comparison(
    comparison,
) -> None:
    """
    Store generated comparison.
    """

    st.session_state.comparison = comparison


def get_comparison():
    """
    Return generated comparison.
    """

    return st.session_state.comparison


def clear_comparison() -> None:
    """
    Remove comparison result.
    """

    st.session_state.comparison = None


# =============================================================================
# Notes
# =============================================================================

def set_notes(
    notes,
) -> None:
    """
    Store generated notes.
    """

    st.session_state.notes = notes


def get_notes():
    """
    Return generated notes.
    """

    return st.session_state.notes


def clear_notes() -> None:
    """
    Remove generated notes.
    """

    st.session_state.notes = None


# =============================================================================
# Reset Helpers
# =============================================================================

def reset_results() -> None:
    """
    Clear all generated AI results.
    """

    clear_summary()

    clear_comparison()

    clear_notes()


def reset_session() -> None:
    """
    Reset application session.
    """

    clear_chat()

    reset_results()

    clear_notifications()

    st.session_state.uploaded_files = []


# =============================================================================
# Session Information
# =============================================================================

def session_duration() -> str:
    """
    Return current session duration.
    """

    delta = datetime.now() - st.session_state.startup_time

    minutes = int(
        delta.total_seconds() // 60
    )

    hours = minutes // 60

    minutes %= 60

    if hours:

        return f"{hours}h {minutes}m"

    return f"{minutes}m"


# =============================================================================
# Startup
# =============================================================================

def startup_completed() -> bool:
    """
    Return startup status.
    """

    return st.session_state.startup_complete


def set_startup_completed(
    value: bool = True,
) -> None:
    """
    Update startup status.
    """

    st.session_state.startup_complete = value
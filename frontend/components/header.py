"""
File: frontend/components/header.py

Enterprise Header Component
"""

from __future__ import annotations

from datetime import datetime

import streamlit as st

from utils.constants import (
    APP_NAME,
    APP_DESCRIPTION,
    APP_VERSION,
    LOGO_PATH,
)


# =============================================================================
# Helpers
# =============================================================================

def _current_time() -> str:
    """
    Return formatted current time.
    """

    return datetime.now().strftime(
        "%d %b %Y • %I:%M %p"
    )


# =============================================================================
# Branding
# =============================================================================

def _render_branding() -> None:
    """
    Render application branding.
    """

    col_logo, col_text = st.columns(
        [1, 8]
    )

    with col_logo:

        if LOGO_PATH.exists():

            st.image(
                str(LOGO_PATH),
                width=80,
            )

    with col_text:

        st.markdown(
            f"""
<h1 class="app-title">

{APP_NAME}

</h1>

<p class="app-description">

{APP_DESCRIPTION}

</p>

<p class="app-version">

Version {APP_VERSION}

</p>
""",
            unsafe_allow_html=True,
        )


# =============================================================================
# Status Banner
# =============================================================================

def _render_status(
    backend_status: str,
) -> None:
    """
    Render backend status.
    """

    status_class = (
        "status-online"
        if backend_status.lower() == "online"
        else "status-offline"
    )

    st.markdown(
        f"""
<div class="status-banner">

<div>

<span class="{status_class}">

{backend_status}

</span>

</div>

<div>

{_current_time()}

</div>

</div>
""",
        unsafe_allow_html=True,
    )


# =============================================================================
# Dashboard Metrics
# =============================================================================

def _render_metrics(
    total_documents: int,
    total_chunks: int,
    total_chats: int,
) -> None:
    """
    Render dashboard metrics.
    """

    col1, col2, col3 = st.columns(
        3
    )

    with col1:

        st.metric(
            "📄 Documents",
            total_documents,
        )

    with col2:

        st.metric(
            "🧩 Chunks",
            total_chunks,
        )

    with col3:

        st.metric(
            "💬 Chats",
            total_chats,
        )


# =============================================================================
# Welcome Banner
# =============================================================================

def _render_banner() -> None:
    """
    Render welcome banner.
    """

    st.markdown(
        """
<div class="hero-card">

<h2>

🚀 Welcome to your Enterprise AI Research Assistant

</h2>

<p>

Upload research papers, ask questions,
generate summaries, compare documents,
and create study notes using RAG.

</p>

</div>
""",
        unsafe_allow_html=True,
    )


# =============================================================================
# Public Component
# =============================================================================

def render_header(
    backend_status: str,
    total_documents: int,
    total_chunks: int,
    total_chats: int,
) -> None:
    """
    Render enterprise header.
    """

    _render_branding()

    st.markdown(
        "<br>",
        unsafe_allow_html=True,
    )

    _render_status(
        backend_status,
    )

    st.markdown(
        "<br>",
        unsafe_allow_html=True,
    )

    _render_metrics(
        total_documents,
        total_chunks,
        total_chats,
    )

    st.markdown(
        "<br>",
        unsafe_allow_html=True,
    )

    _render_banner()

    st.markdown(
        "<hr>",
        unsafe_allow_html=True,
    )
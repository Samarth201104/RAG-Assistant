"""
File: frontend/app.py

Enterprise Entry Point
MultiModal RAG Research Assistant
"""

from __future__ import annotations

from pathlib import Path

import streamlit as st

# =============================================================================
# Components
# =============================================================================

from components.header import render_header
from components.sidebar import render_sidebar

# =============================================================================
# Pages
# =============================================================================

from pages.upload import render_upload_page
from pages.chat import render_chat_page
from pages.summarize import render_summarize_page
from pages.compare import render_compare_page
from pages.notes import render_notes_page

# =============================================================================
# Services
# =============================================================================

from services.data_manager import data_manager
from services.state_manager import state_manager

# =============================================================================
# Utilities
# =============================================================================

from utils.constants import (
    PAGE_TITLE,
    PAGE_ICON,
    LAYOUT,
    INITIAL_SIDEBAR_STATE,
    CSS_PATH,
)

# =============================================================================
# Streamlit Configuration
# =============================================================================

st.set_page_config(

    page_title=PAGE_TITLE,

    page_icon=PAGE_ICON,

    layout=LAYOUT,

    initial_sidebar_state=INITIAL_SIDEBAR_STATE,

)

# =============================================================================
# Load Stylesheet
# =============================================================================

def load_css() -> None:
    """
    Load custom CSS.
    """

    if CSS_PATH.exists():

        st.markdown(

            f"<style>{CSS_PATH.read_text(encoding='utf-8')}</style>",

            unsafe_allow_html=True,

        )


load_css()

# =============================================================================
# Initialize Application State
# =============================================================================

state_manager.initialize()

# =============================================================================
# Load Cached Dashboard Data
# =============================================================================

dashboard = data_manager.dashboard()

state_manager.refresh_dashboard(
    dashboard,
)

# =============================================================================
# Frequently Used Values
# =============================================================================

backend_online = dashboard.get(
    "backend_online",
    False,
)

backend_status = (
    "Connected"
    if backend_online
    else "Offline"
)

document_count = dashboard.get(
    "document_count",
    0,
)

chunk_count = dashboard.get(
    "chunk_count",
    0,
)

documents = dashboard.get(
    "documents",
    [],
)

chat_history = state_manager.get(
    "chat_history",
)

chat_count = len(
    chat_history,
)

# =============================================================================
# Backend Offline Warning
# =============================================================================

if not backend_online:

    st.warning(
        """
Backend server is currently offline.

Please start the FastAPI server before using the application.
"""
    )

# =============================================================================
# Header
# =============================================================================

render_header(
    backend_status=backend_status,
    total_documents=document_count,
    total_chunks=chunk_count,
    total_chats=chat_count,
)

# =============================================================================
# Sidebar
# =============================================================================

selected_page = render_sidebar(
    backend_status=backend_status,
    total_documents=document_count,
    total_chunks=chunk_count,
)

state_manager.set(
    "page",
    selected_page,
)

# =============================================================================
# Hero Section
# =============================================================================

st.markdown(
    """
<div class="hero fade-in">

<h1 class="hero-title">

MultiModal <span>RAG</span> Research Assistant

</h1>

<p class="hero-description">

An enterprise AI platform for semantic document retrieval,
research assistance, intelligent summarization,
document comparison, and study note generation.

Powered by FastAPI, LangChain, Gemini, ChromaDB,
and Streamlit.

</p>

</div>
""",
    unsafe_allow_html=True,
)

# =============================================================================
# Dashboard Metrics
# =============================================================================

st.markdown(
    """
<h2 class="section-title">
Dashboard Overview
</h2>
""",
    unsafe_allow_html=True,
)

metric1, metric2, metric3, metric4 = st.columns(4)

with metric1:

    st.metric(
        "Backend",
        "🟢 Online" if backend_online else "🔴 Offline",
    )

with metric2:

    st.metric(
        "Documents",
        document_count,
    )

with metric3:

    st.metric(
        "Vector Chunks",
        chunk_count,
    )

with metric4:

    st.metric(
        "Chat History",
        chat_count,
    )

# =============================================================================
# Quick Actions
# =============================================================================

st.markdown(
    """
<h2 class="section-title">
Quick Actions
</h2>
""",
    unsafe_allow_html=True,
)

action1, action2, action3, action4, action5 = st.columns(5)

with action1:

    if st.button(
        "📤 Upload",
        use_container_width=True,
    ):

        state_manager.set(
            "page",
            "Upload",
        )

        st.rerun()

with action2:

    if st.button(
        "💬 Chat",
        use_container_width=True,
    ):

        state_manager.set(
            "page",
            "Chat",
        )

        st.rerun()

with action3:

    if st.button(
        "📝 Summarize",
        use_container_width=True,
    ):

        state_manager.set(
            "page",
            "Summarize",
        )

        st.rerun()

with action4:

    if st.button(
        "⚖ Compare",
        use_container_width=True,
    ):

        state_manager.set(
            "page",
            "Compare",
        )

        st.rerun()

with action5:

    if st.button(
        "📚 Notes",
        use_container_width=True,
    ):

        state_manager.set(
            "page",
            "Notes",
        )

        st.rerun()

st.markdown(
    "<br>",
    unsafe_allow_html=True,
)


# =============================================================================
# Page Router
# =============================================================================

try:

    current_page = state_manager.get(
        "page",
    )

    if current_page == "Upload":

        render_upload_page()

    elif current_page == "Chat":

        render_chat_page()

    elif current_page == "Summarize":

        render_summarize_page()

    elif current_page == "Compare":

        render_compare_page()

    elif current_page == "Notes":

        render_notes_page()

    else:

        st.info(
            "Please select a page from the sidebar."
        )

except Exception as error:

    st.markdown(
        """
<div class="empty-state">

<div class="empty-icon">

⚠️

</div>

<div class="empty-title">

Unexpected Error

</div>

<div class="empty-text">

The application encountered an unexpected error.
Please try refreshing the application.

</div>

</div>
""",
        unsafe_allow_html=True,
    )

    with st.expander(
        "Technical Details",
        expanded=False,
    ):

        st.exception(
            error,
        )

# =============================================================================
# Footer
# =============================================================================

st.markdown(
    "<br><br>",
    unsafe_allow_html=True,
)

st.markdown(
    """
<hr style="margin-top:30px;margin-bottom:20px;">
""",
    unsafe_allow_html=True,
)

footer_left, footer_center, footer_right = st.columns(
    [2, 3, 2]
)

with footer_left:

    st.caption(
        "🤖 MultiModal RAG Research Assistant"
    )

with footer_center:

    st.caption(
        "Powered by FastAPI • LangChain • Gemini • ChromaDB • Streamlit"
    )

with footer_right:

    st.caption(
        "Version 1.0.0"
    )

# =============================================================================
# Startup Notification
# =============================================================================

if not state_manager.get(
    "startup_complete",
):

    st.toast(
        "🚀 Enterprise AI Research Platform Ready",
        icon="🤖",
    )

    state_manager.set(
        "startup_complete",
        True,
    )


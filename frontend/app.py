"""
File: frontend/app.py

Enterprise Entry Point
MultiModal RAG Research Assistant
"""

from __future__ import annotations

import streamlit as st

# =============================================================================
# Components
# =============================================================================

from components.header import render_header
from components.sidebar import render_sidebar

# =============================================================================
# Pages
# =============================================================================

from views.upload import render_upload_page
from views.chat import render_chat_page
from views.summarize import render_summarize_page
from views.compare import render_compare_page
from views.notes import render_notes_page

# =============================================================================
# Services
# =============================================================================

from services.api_client import api_client

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

from utils.session import (
    initialize_session,
    get_current_page,
    set_current_page,
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
# Load CSS
# =============================================================================

def load_css() -> None:
    """
    Load custom stylesheet.
    """

    if CSS_PATH.exists():

        st.markdown(

            f"<style>{CSS_PATH.read_text(encoding='utf-8')}</style>",

            unsafe_allow_html=True,

        )


load_css()

# =============================================================================
# Initialize Session
# =============================================================================

initialize_session()

# =============================================================================
# Backend Information
# =============================================================================

backend_online = api_client.backend_available()

backend_status = (

    "🟢 Connected"

    if backend_online

    else "🔴 Offline"

)

# =============================================================================
# Dashboard Data
# =============================================================================

if backend_online:

    summary = api_client.collection_summary()

    documents = summary.get(

        "documents",

        [],

    )

    statistics = summary.get(

        "statistics",

        {},

    )

else:

    documents = []

    statistics = {}

document_count = len(
    documents
)

chunk_count = statistics.get(
    "total_chunks",
    0,
)

# =============================================================================
# Chat Statistics
# =============================================================================

chat_history = st.session_state.get(
    "chat_history",
    [],
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

Please start the FastAPI backend before using
the application.
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

#
# Store current page
#

set_current_page(
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
document comparison and AI-powered study note generation.

Powered by FastAPI, LangChain, Gemini, ChromaDB
and Streamlit.

</p>

</div>
""",

    unsafe_allow_html=True,

)

# =============================================================================
# Dashboard Overview
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

        "🟢 Online"

        if backend_online

        else

        "🔴 Offline",

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

        "Chat Messages",

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

col1, col2, col3, col4, col5 = st.columns(5)

with col1:

    if st.button(

        "📤 Upload",

        use_container_width=True,

    ):

        set_current_page(
            "Upload",
        )

        st.rerun()

with col2:

    if st.button(

        "💬 Chat",

        use_container_width=True,

    ):

        set_current_page(
            "Chat",
        )

        st.rerun()

with col3:

    if st.button(

        "📝 Summarize",

        use_container_width=True,

    ):

        set_current_page(
            "Summarize",
        )

        st.rerun()

with col4:

    if st.button(

        "⚖ Compare",

        use_container_width=True,

    ):

        set_current_page(
            "Compare",
        )

        st.rerun()

with col5:

    if st.button(

        "📚 Notes",

        use_container_width=True,

    ):

        set_current_page(
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

    current_page = get_current_page()

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

Please refresh the application and try again.

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
# Divider
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

# =============================================================================
# Footer
# =============================================================================

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

if not st.session_state.get(
    "startup_complete",
    False,
):

    st.toast(

        "🚀 Enterprise AI Research Platform Ready",

        icon="🤖",

    )

    st.session_state[
        "startup_complete"
    ] = True


# =============================================================================
# Graceful Shutdown
# =============================================================================

try:

    pass

finally:

    try:

        api_client.close()

    except Exception:

        pass
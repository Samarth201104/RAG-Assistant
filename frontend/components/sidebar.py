"""
File: frontend/components/sidebar.py

Enterprise Sidebar Component
"""

from __future__ import annotations

import streamlit as st

from utils.constants import (
    APP_NAME,
    APP_VERSION,
    LOGO_PATH,
    NAVIGATION,
    LLM_MODEL,
    EMBEDDING_MODEL,
    VECTOR_DATABASE,
)

from utils.session import (
    get_current_page,
    set_current_page,
    clear_chat,
    session_duration,
)


# =============================================================================
# Branding
# =============================================================================

def _render_branding() -> None:
    """
    Render sidebar branding.
    """

    st.markdown(
        "<div class='sidebar-brand'>",
        unsafe_allow_html=True,
    )

    if LOGO_PATH.exists():

        st.image(
            str(LOGO_PATH),
            width=70,
        )

    st.markdown(
        f"""
<h2 class="sidebar-title">

{APP_NAME}

</h2>

<p class="sidebar-version">

Version {APP_VERSION}

</p>
""",
        unsafe_allow_html=True,
    )

    st.markdown(
        "</div>",
        unsafe_allow_html=True,
    )


# =============================================================================
# Navigation
# =============================================================================

def _render_navigation() -> str:
    """
    Render navigation.
    """

    st.markdown("### Navigation")

    current_page = get_current_page()

    selected_page = current_page

    for item in NAVIGATION:

        page = item["title"]

        icon = item["icon"]

        button_type = (
            "primary"
            if page == current_page
            else "secondary"
        )

        if st.button(
            f"{icon}  {page}",
            use_container_width=True,
            type=button_type,
            key=f"nav_{page}",
        ):

            selected_page = page

            set_current_page(
                page,
            )

            st.rerun()

    return selected_page


# =============================================================================
# System Information
# =============================================================================

def _render_system_information(
    backend_status: str,
    total_documents: int,
    total_chunks: int,
) -> None:
    """
    Display system information.
    """

    st.markdown("---")

    st.markdown("### System")

    backend_icon = (
        "🟢"
        if backend_status.lower() == "online"
        else "🔴"
    )

    st.markdown(
        f"""
**Backend**

{backend_icon} {backend_status}
"""
    )

    st.markdown(
        f"""
**LLM**

{LLM_MODEL}
"""
    )

    st.markdown(
        f"""
**Embedding**

{EMBEDDING_MODEL}
"""
    )

    st.markdown(
        f"""
**Vector DB**

{VECTOR_DATABASE}
"""
    )

    st.metric(
        "📄 Documents",
        total_documents,
    )

    st.metric(
        "🧩 Chunks",
        total_chunks,
    )

    st.metric(
        "⏱ Session",
        session_duration(),
    )


# =============================================================================
# Quick Actions
# =============================================================================

def _render_quick_actions() -> None:
    """
    Sidebar actions.
    """

    st.markdown("---")

    st.markdown("### Quick Actions")

    if st.button(
        "🧹 Clear Chat",
        use_container_width=True,
    ):

        clear_chat()

        st.success(
            "Conversation cleared."
        )

    if st.button(
        "🔄 Refresh",
        use_container_width=True,
    ):

        st.cache_data.clear()

        st.rerun()


# =============================================================================
# Footer
# =============================================================================

def _render_footer() -> None:
    """
    Sidebar footer.
    """

    st.markdown("---")

    st.markdown(
        """
<div class="sidebar-footer">

Built with

<br>

🚀 FastAPI

<br>

🦜 LangChain

<br>

✨ Gemini

<br>

🗄 ChromaDB

<br>

🎈 Streamlit

</div>
""",
        unsafe_allow_html=True,
    )


# =============================================================================
# Public Component
# =============================================================================

def render_sidebar(
    backend_status: str,
    total_documents: int,
    total_chunks: int,
) -> str:
    """
    Render enterprise sidebar.

    Returns
    -------
    str
        Selected page.
    """

    with st.sidebar:

        _render_branding()

        selected_page = _render_navigation()

        _render_system_information(
            backend_status,
            total_documents,
            total_chunks,
        )

        _render_quick_actions()

        _render_footer()

    return selected_page
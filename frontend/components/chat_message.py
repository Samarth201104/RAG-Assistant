"""
File: frontend/components/chat_message.py

Enterprise Chat Message Component
"""

from __future__ import annotations

from datetime import datetime

import streamlit as st

from utils.constants import (
    AI_AVATAR,
    USER_AVATAR,
)


# =============================================================================
# Helpers
# =============================================================================

def _timestamp() -> str:
    """
    Return current timestamp.
    """

    return datetime.now().strftime(
        "%I:%M %p"
    )


# =============================================================================
# Message Header
# =============================================================================

def _message_header(
    avatar: str,
    title: str,
) -> None:
    """
    Render message header.
    """

    st.markdown(
        f"""
<div class="message-header">

<div class="message-author">

<span class="message-avatar">

{avatar}

</span>

<span class="message-name">

{title}

</span>

</div>

<div class="message-time">

{_timestamp()}

</div>

</div>
""",
        unsafe_allow_html=True,
    )


# =============================================================================
# User Message
# =============================================================================

def render_user_message(
    message: str,
) -> None:
    """
    Render user chat message.
    """

    with st.container():

        st.markdown(
            '<div class="chat-user">',
            unsafe_allow_html=True,
        )

        _message_header(
            USER_AVATAR,
            "You",
        )

        st.markdown(message)

        st.markdown(
            "</div>",
            unsafe_allow_html=True,
        )


# =============================================================================
# Assistant Message
# =============================================================================

def render_ai_message(
    message: str,
) -> None:
    """
    Render AI chat message.
    """

    with st.container():

        st.markdown(
            '<div class="chat-ai">',
            unsafe_allow_html=True,
        )

        _message_header(
            AI_AVATAR,
            "AI Assistant",
        )

        st.markdown(
            message,
            unsafe_allow_html=False,
        )

        st.markdown(
            "</div>",
            unsafe_allow_html=True,
        )


# =============================================================================
# Markdown Renderer
# =============================================================================

def render_markdown(
    content: str,
) -> None:
    """
    Render markdown.
    """

    st.markdown(
        content,
        unsafe_allow_html=False,
    )


# =============================================================================
# Code Renderer
# =============================================================================

def render_code(
    code: str,
    language: str = "python",
) -> None:
    """
    Render syntax highlighted code.
    """

    st.code(
        code,
        language=language,
    )


# =============================================================================
# Message Divider
# =============================================================================

def render_divider() -> None:
    """
    Render divider between messages.
    """

    st.markdown(
        "<hr>",
        unsafe_allow_html=True,
    )

# =============================================================================
# Copy Response
# =============================================================================

def render_copy_response(
    response: str,
) -> None:
    """
    Render a copyable response block.
    """

    with st.expander(
        "📋 Copy Response",
        expanded=False,
    ):

        st.code(
            response,
            language=None,
        )


# =============================================================================
# Typing Indicator
# =============================================================================

def render_typing_indicator() -> None:
    """
    Display ChatGPT-style typing animation.
    """

    st.markdown(
        """
<div class="typing-indicator">

<div class="typing-dot"></div>

<div class="typing-dot"></div>

<div class="typing-dot"></div>

</div>
""",
        unsafe_allow_html=True,
    )


# =============================================================================
# Citations
# =============================================================================

def render_citations(
    citations: list | None,
) -> None:
    """
    Render citations below AI response.
    """

    if not citations:

        return

    st.markdown("### 📚 Sources")

    for index, citation in enumerate(
        citations,
        start=1,
    ):

        source = citation.get(
            "source",
            "Unknown",
        )

        page = citation.get(
            "page",
            "-",
        )

        chunk = citation.get(
            "chunk",
            "-",
        )

        confidence = citation.get(
            "confidence",
            None,
        )

        preview = citation.get(
            "preview",
            "",
        )

        confidence_text = (
            f"{confidence:.0%}"
            if isinstance(
                confidence,
                (int, float),
            )
            else "N/A"
        )

        with st.expander(
            f"📄 Source {index}: {source}",
            expanded=False,
        ):

            col1, col2, col3 = st.columns(3)

            with col1:

                st.caption(
                    f"Page: {page}"
                )

            with col2:

                st.caption(
                    f"Chunk: {chunk}"
                )

            with col3:

                st.caption(
                    f"Confidence: {confidence_text}"
                )

            if preview:

                st.markdown(
                    preview
                )


# =============================================================================
# Response Toolbar
# =============================================================================

def render_toolbar(
    response: str,
) -> None:
    """
    Render response tools.
    """

    col1, col2 = st.columns(
        [1, 1]
    )

    with col1:

        render_copy_response(
            response,
        )

    with col2:

        st.button(
            "🔄 Regenerate",
            disabled=True,
            use_container_width=True,
            help="Coming soon",
        )


# =============================================================================
# Complete Chat Message
# =============================================================================

def render_chat_message(
    role: str,
    message: str,
    citations: list | None = None,
) -> None:
    """
    Render complete chat message.
    """

    role = role.lower()

    if role == "user":

        render_user_message(
            message,
        )

        return

    render_ai_message(
        message,
    )

    render_toolbar(
        message,
    )

    render_citations(
        citations,
    )

    render_divider()
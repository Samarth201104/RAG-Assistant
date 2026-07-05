"""
File: frontend/pages/chat.py

Enterprise Chat Page
"""

from __future__ import annotations

import streamlit as st

from components.loading import (
    loading_context,
    loading_error,
)

from components.chat_message import (
    render_chat_message,
)

from components.citation_card import (
    render_citation_section,
)

from services.api_client import (
    api_client,
)

from utils.helpers import (
    page_title,
)

from utils.session import (
    get_chat_history,
    set_chat_history,
    clear_chat,
)


# =============================================================================
# Suggested Questions
# =============================================================================

SUGGESTED_QUESTIONS = [

    "Summarize the uploaded research paper.",

    "What is the main contribution of the paper?",

    "Explain the proposed methodology.",

    "List the important findings.",

    "What are the limitations of the paper?",

    "Explain this paper in simple language.",

    "Generate interview questions from this paper.",

    "Compare the concepts discussed in the paper.",

]


# =============================================================================
# Welcome Screen
# =============================================================================

def _render_welcome() -> None:
    """
    Render welcome screen.
    """

    st.markdown(
        """
<div class="hero">

<h2>

💬 AI Research Assistant

</h2>

<p>

Ask questions about your uploaded documents.

Powered by Retrieval-Augmented Generation (RAG).

</p>

</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown(
        "### 🚀 Suggested Questions"
    )

    cols = st.columns(2)

    for index, question in enumerate(
        SUGGESTED_QUESTIONS
    ):

        column = cols[index % 2]

        with column:

            if st.button(

                question,

                use_container_width=True,

                key=f"suggestion_{index}",

            ):

                st.session_state[
                    "chat_input"
                ] = question

                st.rerun()


# =============================================================================
# Chat History
# =============================================================================

def _render_chat_history() -> None:
    """
    Render chat history.
    """

    history = get_chat_history()

    if not history:

        _render_welcome()

        return

    for message in history:

        render_chat_message(

            role=message.get(
                "role",
                "assistant",
            ),

            message=message.get(
                "content",
                "",
            ),

            citations=message.get(
                "citations",
                [],
            ),

        )


# =============================================================================
# Chat Toolbar
# =============================================================================

def _render_toolbar() -> None:
    """
    Chat actions.
    """

    col1, col2 = st.columns(
        [2, 8]
    )

    with col1:

        if st.button(

            "🗑 Clear Chat",

            use_container_width=True,

        ):

            clear_chat()

            st.rerun()

    with col2:

        st.info(

            "Responses are generated using the indexed documents in your knowledge base."

        )


# =============================================================================
# Header
# =============================================================================

def _render_header() -> None:
    """
    Render page title.
    """

    page_title(

        "💬 AI Chat",

        "Ask questions about your uploaded PDF documents and images.",

    )

# =============================================================================
# Query Backend
# =============================================================================

def _query_backend(
    question: str,
) -> bool:
    """
    Query the RAG backend.
    """

    try:

        with loading_context(
            "Thinking..."
        ):

            response = api_client.query(
                question=question,
            )

        if not response.get(
            "success",
            False,
        ):

            loading_error(
                response.get(
                    "message",
                    "Unable to generate response.",
                )
            )

            return False

        result = response.get(
            "data",
            {},
        )

        #
        # Backend normalization
        #

        if isinstance(
            result,
            dict,
        ):

            answer = (

                result.get("answer")

                or result.get("response")

                or result.get("output")

                or ""

            )

            citations = (

                result.get("citations")

                or result.get("sources")

                or []

            )

        else:

            answer = str(result)

            citations = []

        history = get_chat_history()

        history.append(

            {

                "role": "user",

                "content": question,

            }

        )

        history.append(

            {

                "role": "assistant",

                "content": answer,

                "citations": citations,

            }

        )

        set_chat_history(
            history,
        )

        return True

    except Exception as error:

        loading_error(
            str(error),
        )

        return False


# =============================================================================
# Chat Input
# =============================================================================

def _render_chat_input() -> None:
    """
    Render chat input.
    """

    default_prompt = st.session_state.pop(
        "chat_input",
        "",
    )

    question = st.chat_input(

        "Ask a question about your documents...",

        key="chat_box",

    )

    #
    # Suggested question clicked
    #

    if default_prompt:

        question = default_prompt

    if not question:

        return

    success = _query_backend(
        question,
    )

    if success:

        st.rerun()


# =============================================================================
# Response Viewer
# =============================================================================

def _render_last_sources() -> None:
    """
    Display citations of the latest response.
    """

    history = get_chat_history()

    if not history:

        return

    last = history[-1]

    if last.get(
        "role",
    ) != "assistant":

        return

    citations = last.get(
        "citations",
        [],
    )

    if citations:

        st.markdown("---")

        render_citation_section(
            citations,
        )


# =============================================================================
# Empty Database Warning
# =============================================================================

def _render_database_warning() -> None:
    """
    Warn user if no documents exist.
    """

    documents = api_client.list_documents()

    if documents:

        return

    st.warning(

        """
No indexed documents were found.

Please upload one or more PDF documents before
asking questions.
"""

    )

# =============================================================================
# Chat Page
# =============================================================================

def render_chat_page() -> None:
    """
    Render enterprise AI chat page.
    """

    _render_header()

    st.markdown(
        "<br>",
        unsafe_allow_html=True,
    )

    _render_database_warning()

    st.markdown(
        "<br>",
        unsafe_allow_html=True,
    )

    _render_toolbar()

    st.markdown(
        "<br>",
        unsafe_allow_html=True,
    )

    chat_container = st.container()

    with chat_container:

        _render_chat_history()

    st.markdown(
        "<br>",
        unsafe_allow_html=True,
    )

    _render_chat_input()

    st.markdown(
        "<br>",
        unsafe_allow_html=True,
    )

    _render_last_sources()


# =============================================================================
# Chat Statistics
# =============================================================================

def render_chat_statistics() -> None:
    """
    Display chat statistics.
    """

    history = get_chat_history()

    if not history:

        return

    user_messages = sum(

        1

        for message in history

        if message.get("role") == "user"

    )

    assistant_messages = sum(

        1

        for message in history

        if message.get("role") == "assistant"

    )

    total_sources = sum(

        len(

            message.get(
                "citations",
                [],
            )

        )

        for message in history

        if message.get("role") == "assistant"

    )

    st.markdown("---")

    st.markdown(
        "### 📊 Conversation Statistics"
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Questions",
            user_messages,
        )

    with col2:

        st.metric(
            "Responses",
            assistant_messages,
        )

    with col3:

        st.metric(
            "Sources",
            total_sources,
        )


# =============================================================================
# Export Conversation
# =============================================================================

def export_chat_history() -> None:
    """
    Download conversation.
    """

    history = get_chat_history()

    if not history:

        return

    conversation = []

    for message in history:

        role = message.get(
            "role",
            "assistant",
        ).upper()

        content = message.get(
            "content",
            "",
        )

        conversation.append(
            f"{role}\n{'-' * 40}\n{content}\n"
        )

    st.download_button(

        label="📥 Export Conversation",

        data="\n\n".join(
            conversation,
        ),

        file_name="chat_history.txt",

        mime="text/plain",

        use_container_width=True,

    )


# =============================================================================
# Sidebar Utilities
# =============================================================================

def render_chat_sidebar() -> None:
    """
    Optional chat utilities.
    Can be called from app.py if desired.
    """

    history = get_chat_history()

    if not history:

        return

    st.sidebar.markdown("---")

    st.sidebar.markdown(
        "### 💬 Chat"
    )

    st.sidebar.metric(
        "Messages",
        len(history),
    )

    if st.sidebar.button(
        "📥 Export Chat",
        use_container_width=True,
    ):

        export_chat_history()

    if st.sidebar.button(
        "🗑 Clear Conversation",
        use_container_width=True,
    ):

        clear_chat()

        st.rerun()
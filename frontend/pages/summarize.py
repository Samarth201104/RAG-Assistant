"""
File: frontend/pages/summarize.py

Enterprise Document Summarization Page
"""

from __future__ import annotations

import streamlit as st

from components.loading import (
    loading_error,
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
    get_summary,
    set_summary,
)


# =============================================================================
# Summary Types
# =============================================================================

SUMMARY_TYPES = {

    "Complete Summary": api_client.summarize,

    "Executive Summary": api_client.executive_summary,

    "Key Findings": api_client.key_findings,

    "Methodology": api_client.methodology_summary,

    "Limitations": api_client.limitations_summary,

    "Future Work": api_client.future_work_summary,

    "Contribution": api_client.contribution_summary,

    "Abstract": api_client.abstract_summary,

    "One Line Summary": api_client.one_line_summary,

    "TL;DR": api_client.tldr_summary,

    "Complete Summary Package": api_client.complete_summary,

}


# =============================================================================
# Header
# =============================================================================

def _render_header() -> None:
    """
    Render page header.
    """

    page_title(

        "📝 AI Document Summarization",

        (
            "Generate intelligent summaries from your "
            "indexed research papers using Gemini AI."
        ),

    )


# =============================================================================
# Load Documents
# =============================================================================

def _load_documents() -> list[str]:
    """
    Load indexed documents.
    """

    try:

        documents = api_client.list_documents()

        if not documents:

            return []

        filenames = []

        for document in documents:

            if isinstance(
                document,
                dict,
            ):

                filenames.append(

                    document.get(
                        "filename",
                        "Unknown",
                    )

                )

            else:

                filenames.append(
                    str(document)
                )

        return sorted(filenames)

    except Exception as error:

        loading_error(
            str(error)
        )

        return []


# =============================================================================
# Document Selector
# =============================================================================

def _render_document_selector(
    documents: list[str],
) -> str | None:
    """
    Render document selector.
    """

    st.markdown(
        "### 📄 Select Document"
    )

    if not documents:

        st.info(
            "No indexed documents available."
        )

        return None

    return st.selectbox(

        "Document",

        options=documents,

        label_visibility="collapsed",

    )


# =============================================================================
# Summary Selector
# =============================================================================

def _render_summary_selector() -> tuple[str, callable]:
    """
    Select summary type.
    """

    st.markdown(
        "### 🤖 Summary Type"
    )

    summary_name = st.selectbox(

        "Summary",

        list(
            SUMMARY_TYPES.keys()
        ),

        label_visibility="collapsed",

    )

    return (

        summary_name,

        SUMMARY_TYPES[
            summary_name
        ],

    )


# =============================================================================
# Generate Button
# =============================================================================

def _render_generate_button() -> bool:
    """
    Generate summary button.
    """

    st.markdown(
        "<br>",
        unsafe_allow_html=True,
    )

    return st.button(

        "🚀 Generate Summary",

        type="primary",

        use_container_width=True,

    )


# =============================================================================
# Previous Result
# =============================================================================

def _render_previous_summary() -> None:
    """
    Display existing summary.
    """

    summary = get_summary()

    if not summary:

        return

    st.markdown("---")

    st.markdown(
        "## 📑 Generated Summary"
    )

    if isinstance(
        summary,
        dict,
    ):

        response = summary.get(
            "response",
            summary,
        )

        if isinstance(
            response,
            dict,
        ):

            st.json(
                response
            )

        else:

            st.markdown(
                str(response)
            )

        citations = summary.get(
            "citations",
            [],
        )

        if citations:

            render_citation_section(
                citations
            )

    else:

        st.markdown(
            str(summary)
        )

# =============================================================================
# Generate Summary
# =============================================================================

def _generate_summary(
    filename: str,
    summary_function,
) -> bool:
    """
    Generate AI summary.
    """

    try:

        with st.spinner(
            "Generating AI summary..."
        ):

            response = summary_function(
                filename,
            )

        if not response.get(
            "success",
            False,
        ):

            loading_error(

                response.get(
                    "message",
                    "Summary generation failed.",
                )

            )

            return False

        result = response.get(
            "data",
            {},
        )

        #
        # Normalize backend response
        #

        if isinstance(
            result,
            dict,
        ):

            summary = (

                result.get("summary")

                or result.get("response")

                or result.get("output")

                or result

            )

            citations = (

                result.get("citations")

                or result.get("sources")

                or []

            )

        else:

            summary = str(result)

            citations = []

        set_summary(

            {

                "response": summary,

                "citations": citations,

            }

        )

        return True

    except Exception as error:

        loading_error(
            str(error),
        )

        return False


# =============================================================================
# Action Panel
# =============================================================================

def _render_action_panel(
    filename: str | None,
    summary_function,
) -> None:
    """
    Summary generation actions.
    """

    if filename is None:

        return

    if _render_generate_button():

        success = _generate_summary(

            filename,

            summary_function,

        )

        if success:

            st.toast(

                "Summary generated successfully.",

                icon="✅",

            )

            st.rerun()


# =============================================================================
# Export Summary
# =============================================================================

def _render_export() -> None:
    """
    Export generated summary.
    """

    summary = get_summary()

    if not summary:

        return

    st.markdown("---")

    st.markdown(
        "### 📥 Export"
    )

    response = summary.get(
        "response",
        "",
    )

    if isinstance(
        response,
        dict,
    ):

        export_text = str(
            response,
        )

    else:

        export_text = str(
            response,
        )

    col1, col2 = st.columns(
        2,
    )

    with col1:

        st.download_button(

            label="📄 Download Summary",

            data=export_text,

            file_name="summary.txt",

            mime="text/plain",

            use_container_width=True,

        )

    with col2:

        st.button(

            "📋 Copy Summary",

            disabled=True,

            use_container_width=True,

            help="Coming soon",

        )


# =============================================================================
# Summary Statistics
# =============================================================================

def _render_statistics() -> None:
    """
    Display summary statistics.
    """

    summary = get_summary()

    if not summary:

        return

    response = str(

        summary.get(
            "response",
            "",
        )

    )

    words = len(
        response.split()
    )

    characters = len(
        response
    )

    citations = len(

        summary.get(
            "citations",
            [],
        )

    )

    st.markdown("---")

    st.markdown(
        "### 📊 Summary Statistics"
    )

    col1, col2, col3 = st.columns(
        3,
    )

    with col1:

        st.metric(
            "Words",
            words,
        )

    with col2:

        st.metric(
            "Characters",
            characters,
        )

    with col3:

        st.metric(
            "Sources",
            citations,
        )

# =============================================================================
# Summarization Page
# =============================================================================

def render_summarize_page() -> None:
    """
    Render enterprise document summarization page.
    """

    _render_header()

    documents = _load_documents()

    if not documents:

        st.warning(
            """
No indexed documents were found.

Please upload one or more PDF documents before
generating summaries.
"""
        )

        return

    st.markdown(
        "<br>",
        unsafe_allow_html=True,
    )

    selected_document = _render_document_selector(
        documents,
    )

    st.markdown(
        "<br>",
        unsafe_allow_html=True,
    )

    summary_name, summary_function = (
        _render_summary_selector()
    )

    st.info(
        f"Selected Summary Type : **{summary_name}**"
    )

    st.markdown(
        "<br>",
        unsafe_allow_html=True,
    )

    _render_action_panel(
        selected_document,
        summary_function,
    )

    st.markdown(
        "<br>",
        unsafe_allow_html=True,
    )

    _render_previous_summary()

    st.markdown(
        "<br>",
        unsafe_allow_html=True,
    )

    _render_statistics()

    st.markdown(
        "<br>",
        unsafe_allow_html=True,
    )

    _render_export()


# =============================================================================
# Sidebar Summary Statistics
# =============================================================================

def render_summary_sidebar() -> None:
    """
    Optional sidebar summary information.
    """

    summary = get_summary()

    if not summary:

        return

    st.sidebar.markdown("---")

    st.sidebar.markdown(
        "### 📝 Summary"
    )

    response = str(
        summary.get(
            "response",
            "",
        )
    )

    st.sidebar.metric(
        "Words",
        len(
            response.split()
        ),
    )

    st.sidebar.metric(
        "Characters",
        len(
            response
        ),
    )

    st.sidebar.metric(
        "Sources",
        len(
            summary.get(
                "citations",
                [],
            )
        ),
    )

    if st.sidebar.button(
        "🗑 Clear Summary",
        use_container_width=True,
    ):

        set_summary(
            {},
        )

        st.rerun()
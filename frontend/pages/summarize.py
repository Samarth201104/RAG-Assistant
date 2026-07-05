"""
File: frontend/pages/summarize.py

Enterprise Document Summarization Page
"""

from __future__ import annotations

import streamlit as st

from components.loading import (
    loading_context,
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
    set_summary,
    get_summary,
)


# =============================================================================
# Page Header
# =============================================================================

def _render_header() -> None:
    """
    Render page heading.
    """

    page_title(
        "📝 Document Summarization",
        (
            "Generate AI-powered summaries from your "
            "indexed research papers."
        ),
    )


# =============================================================================
# Load Documents
# =============================================================================

def _load_documents() -> list[str]:
    """
    Load indexed documents from backend.
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
            str(error),
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

        documents,

        label_visibility="collapsed",

    )


# =============================================================================
# Summary Type
# =============================================================================

SUMMARY_TYPES = {

    "Complete Summary": "",

    "Executive Summary": "executive",

    "Key Findings": "key-findings",

    "Methodology": "methodology",

    "Limitations": "limitations",

    "Future Work": "future-work",

    "Contribution": "contribution",

    "Abstract": "abstract",

    "One Line Summary": "one-line",

    "TLDR": "tldr",

    "Complete Summary Package": "all",

}


def _render_summary_type() -> tuple[str, str]:
    """
    Render summary type selector.

    Returns
    -------
    tuple
        (label, endpoint)
    """

    st.markdown(
        "### 🤖 Summary Type"
    )

    label = st.selectbox(

        "Summary Type",

        list(
            SUMMARY_TYPES.keys()
        ),

        label_visibility="collapsed",

    )

    return (

        label,

        SUMMARY_TYPES[label],

    )


# =============================================================================
# Generate Button
# =============================================================================

def _render_generate_button() -> bool:
    """
    Render generate button.
    """

    st.markdown(
        "<br>",
        unsafe_allow_html=True,
    )

    return st.button(

        "🚀 Generate Summary",

        use_container_width=True,

        type="primary",

    )


# =============================================================================
# Result Viewer
# =============================================================================

def _render_summary_result() -> None:
    """
    Render previously generated summary.
    """

    summary = get_summary()

    if not summary:

        return

    st.markdown(
        "---"
    )

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
                response,
            )

        else:

            st.markdown(
                str(response),
            )

        citations = summary.get(
            "citations",
            [],
        )

        if citations:

            render_citation_section(
                citations,
            )

    else:

        st.markdown(
            str(summary),
        )
"""
File: frontend/pages/compare.py

Enterprise Document Comparison Page
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
    get_comparison,
    set_comparison,
)


# =============================================================================
# Comparison Types
# =============================================================================

COMPARISON_TYPES = {

    "Complete Comparison": api_client.compare,

    "Similarities": api_client.similarities,

    "Differences": api_client.differences,

    "Methodology Comparison": api_client.methodology_comparison,

    "Results Comparison": api_client.results_comparison,

    "Advantages & Limitations": api_client.advantages_limitations,

    "Best Paper": api_client.best_paper,

    "Technical Comparison": api_client.technical_comparison,

    "Comparison Table": api_client.comparison_table,

    "Complete Comparison Package": api_client.complete_comparison,

}


# =============================================================================
# Header
# =============================================================================

def _render_header() -> None:
    """
    Render page title.
    """

    page_title(

        "⚖ AI Document Comparison",

        (
            "Compare two indexed research papers "
            "using Gemini AI."
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
            str(error),
        )

        return []


# =============================================================================
# Document Selection
# =============================================================================

def _render_document_selector(
    documents: list[str],
) -> tuple[str | None, str | None]:
    """
    Select two documents.
    """

    st.markdown(
        "### 📄 Select Documents"
    )

    if len(documents) < 2:

        st.info(
            "At least two indexed documents are required."
        )

        return None, None

    col1, col2 = st.columns(2)

    with col1:

        document_one = st.selectbox(

            "Document 1",

            documents,

        )

    with col2:

        remaining = [

            document

            for document in documents

            if document != document_one

        ]

        document_two = st.selectbox(

            "Document 2",

            remaining,

        )

    return (

        document_one,

        document_two,

    )


# =============================================================================
# Comparison Type
# =============================================================================

def _render_comparison_selector() -> tuple[str, callable]:
    """
    Select comparison type.
    """

    st.markdown(
        "### 🤖 Comparison Type"
    )

    comparison_name = st.selectbox(

        "Comparison",

        list(
            COMPARISON_TYPES.keys()
        ),

        label_visibility="collapsed",

    )

    return (

        comparison_name,

        COMPARISON_TYPES[
            comparison_name
        ],

    )


# =============================================================================
# Compare Button
# =============================================================================

def _render_compare_button() -> bool:
    """
    Compare button.
    """

    st.markdown(
        "<br>",
        unsafe_allow_html=True,
    )

    return st.button(

        "⚖ Compare Documents",

        type="primary",

        use_container_width=True,

    )


# =============================================================================
# Previous Comparison
# =============================================================================

def _render_previous_comparison() -> None:
    """
    Render previous comparison.
    """

    comparison = get_comparison()

    if not comparison:

        return

    st.markdown("---")

    st.markdown(
        "## 📊 Comparison Result"
    )

    if isinstance(
        comparison,
        dict,
    ):

        response = comparison.get(

            "response",

            comparison,

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

        citations = comparison.get(

            "citations",

            [],

        )

        if citations:

            render_citation_section(
                citations,
            )

    else:

        st.markdown(
            str(comparison),
        )

# =============================================================================
# Generate Comparison
# =============================================================================

def _generate_comparison(
    document_one: str,
    document_two: str,
    comparison_function,
) -> bool:
    """
    Generate AI comparison.
    """

    try:

        with st.spinner(
            "Comparing documents..."
        ):

            response = comparison_function(
                document_one,
                document_two,
            )

        if not response.get(
            "success",
            False,
        ):

            loading_error(

                response.get(
                    "message",
                    "Comparison failed.",
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

            comparison = (

                result.get("comparison")

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

            comparison = str(result)

            citations = []

        set_comparison(

            {

                "response": comparison,

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
    document_one: str | None,
    document_two: str | None,
    comparison_function,
) -> None:
    """
    Render comparison action panel.
    """

    if document_one is None:

        return

    if document_two is None:

        return

    if _render_compare_button():

        success = _generate_comparison(

            document_one,

            document_two,

            comparison_function,

        )

        if success:

            st.toast(

                "Comparison completed successfully.",

                icon="✅",

            )

            st.rerun()


# =============================================================================
# Export Comparison
# =============================================================================

def _render_export() -> None:
    """
    Export generated comparison.
    """

    comparison = get_comparison()

    if not comparison:

        return

    st.markdown("---")

    st.markdown(
        "### 📥 Export"
    )

    response = comparison.get(
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

    col1, col2 = st.columns(2)

    with col1:

        st.download_button(

            label="📄 Download Comparison",

            data=export_text,

            file_name="comparison.txt",

            mime="text/plain",

            use_container_width=True,

        )

    with col2:

        st.button(

            "📋 Copy Comparison",

            disabled=True,

            use_container_width=True,

            help="Coming soon",

        )


# =============================================================================
# Comparison Statistics
# =============================================================================

def _render_statistics() -> None:
    """
    Display comparison statistics.
    """

    comparison = get_comparison()

    if not comparison:

        return

    response = str(

        comparison.get(
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

        comparison.get(
            "citations",
            [],
        )

    )

    st.markdown("---")

    st.markdown(
        "### 📊 Comparison Statistics"
    )

    col1, col2, col3 = st.columns(3)

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
# Compare Page
# =============================================================================

def render_compare_page() -> None:
    """
    Render enterprise document comparison page.
    """

    _render_header()

    documents = _load_documents()

    if len(documents) < 2:

        st.warning(
            """
At least two indexed documents are required for comparison.

Please upload more documents before using this feature.
"""
        )

        return

    st.markdown(
        "<br>",
        unsafe_allow_html=True,
    )

    document_one, document_two = _render_document_selector(
        documents,
    )

    st.markdown(
        "<br>",
        unsafe_allow_html=True,
    )

    comparison_name, comparison_function = (
        _render_comparison_selector()
    )

    st.info(
        f"Selected Comparison Type : **{comparison_name}**"
    )

    st.markdown(
        "<br>",
        unsafe_allow_html=True,
    )

    _render_action_panel(
        document_one,
        document_two,
        comparison_function,
    )

    st.markdown(
        "<br>",
        unsafe_allow_html=True,
    )

    _render_previous_comparison()

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
# Sidebar Comparison Statistics
# =============================================================================

def render_compare_sidebar() -> None:
    """
    Optional sidebar comparison information.
    """

    comparison = get_comparison()

    if not comparison:

        return

    st.sidebar.markdown("---")

    st.sidebar.markdown(
        "### ⚖ Comparison"
    )

    response = str(
        comparison.get(
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
            comparison.get(
                "citations",
                [],
            )
        ),
    )

    if st.sidebar.button(
        "🗑 Clear Comparison",
        use_container_width=True,
    ):

        set_comparison(
            {},
        )

        st.rerun()


# =============================================================================
# Comparison Utilities
# =============================================================================

def export_comparison() -> None:
    """
    Export comparison text.
    """

    comparison = get_comparison()

    if not comparison:

        return

    response = comparison.get(
        "response",
        "",
    )

    st.download_button(

        label="📥 Export Comparison",

        data=str(response),

        file_name="comparison.txt",

        mime="text/plain",

        use_container_width=True,

    )


def comparison_available() -> bool:
    """
    Check whether a comparison exists.
    """

    comparison = get_comparison()

    return bool(comparison)
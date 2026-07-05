"""
File: frontend/pages/notes.py

Enterprise Study Notes Generation Page
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
    get_notes,
    set_notes,
)


# =============================================================================
# Note Types
# =============================================================================

NOTE_TYPES = {

    "Study Notes": api_client.generate_notes,

    "Short Notes": api_client.short_notes,

    "Detailed Notes": api_client.detailed_notes,

    "Flashcards": api_client.flashcards,

    "Interview Questions": api_client.interview_questions,

    "Viva Questions": api_client.viva_questions,

    "MCQs": api_client.mcqs,

    "Revision Notes": api_client.revision_notes,

    "Cheat Sheet": api_client.cheat_sheet,

    "Mind Map": api_client.mind_map,

    "FAQs": api_client.faqs,

    "Exam Preparation": api_client.exam_preparation,

    "Concept Explanation": api_client.concept_explanation,

    "Complete Study Package": api_client.complete_notes,

}


# =============================================================================
# Header
# =============================================================================

def _render_header() -> None:
    """
    Render page title.
    """

    page_title(

        "📚 AI Study Notes Generator",

        (
            "Generate intelligent study notes, flashcards, "
            "MCQs, interview questions and more from your "
            "indexed research documents."
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
# Document Selector
# =============================================================================

def _render_document_selector(
    documents: list[str],
) -> str | None:
    """
    Select document.
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
# Note Type Selector
# =============================================================================

def _render_note_selector() -> tuple[str, callable]:
    """
    Select note type.
    """

    st.markdown(
        "### 🤖 Note Type"
    )

    note_name = st.selectbox(

        "Notes",

        list(
            NOTE_TYPES.keys()
        ),

        label_visibility="collapsed",

    )

    return (

        note_name,

        NOTE_TYPES[
            note_name
        ],

    )


# =============================================================================
# Generate Button
# =============================================================================

def _render_generate_button() -> bool:
    """
    Generate notes button.
    """

    st.markdown(
        "<br>",
        unsafe_allow_html=True,
    )

    return st.button(

        "📚 Generate Notes",

        type="primary",

        use_container_width=True,

    )


# =============================================================================
# Previous Notes
# =============================================================================

def _render_previous_notes() -> None:
    """
    Display previously generated notes.
    """

    notes = get_notes()

    if not notes:

        return

    st.markdown("---")

    st.markdown(
        "## 📖 Generated Notes"
    )

    if isinstance(
        notes,
        dict,
    ):

        response = notes.get(

            "response",

            notes,

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

        citations = notes.get(

            "citations",

            [],

        )

        if citations:

            render_citation_section(
                citations,
            )

    else:

        st.markdown(
            str(notes),
        )

# =============================================================================
# Generate Notes
# =============================================================================

def _generate_notes(
    filename: str,
    note_name: str,
    note_function,
) -> bool:
    """
    Generate AI study notes.
    """

    try:

        with st.spinner(
            "Generating AI study notes..."
        ):

            #
            # Default endpoint requires note_type
            #

            if note_function == api_client.generate_notes:

                response = note_function(
                    filename,
                    note_name,
                )

            else:

                response = note_function(
                    filename,
                )

        if not response.get(
            "success",
            False,
        ):

            loading_error(

                response.get(
                    "message",
                    "Notes generation failed.",
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

            notes = (

                result.get("notes")

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

            notes = str(result)

            citations = []

        set_notes(

            {

                "response": notes,

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
    note_name: str,
    note_function,
) -> None:
    """
    Notes generation actions.
    """

    if filename is None:

        return

    if _render_generate_button():

        success = _generate_notes(

            filename,

            note_name,

            note_function,

        )

        if success:

            st.toast(

                "Study notes generated successfully.",

                icon="✅",

            )

            st.rerun()


# =============================================================================
# Export Notes
# =============================================================================

def _render_export() -> None:
    """
    Export generated notes.
    """

    notes = get_notes()

    if not notes:

        return

    st.markdown("---")

    st.markdown(
        "### 📥 Export"
    )

    response = notes.get(
        "response",
        "",
    )

    export_text = str(
        response,
    )

    col1, col2 = st.columns(2)

    with col1:

        st.download_button(

            label="📄 Download Notes",

            data=export_text,

            file_name="study_notes.txt",

            mime="text/plain",

            use_container_width=True,

        )

    with col2:

        st.button(

            "📋 Copy Notes",

            disabled=True,

            use_container_width=True,

            help="Coming soon",

        )


# =============================================================================
# Notes Statistics
# =============================================================================

def _render_statistics() -> None:
    """
    Display notes statistics.
    """

    notes = get_notes()

    if not notes:

        return

    response = str(

        notes.get(
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

        notes.get(
            "citations",
            [],
        )

    )

    st.markdown("---")

    st.markdown(
        "### 📊 Notes Statistics"
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
# Notes Page
# =============================================================================

def render_notes_page() -> None:
    """
    Render enterprise study notes page.
    """

    _render_header()

    documents = _load_documents()

    if not documents:

        st.warning(
            """
No indexed documents were found.

Please upload one or more PDF documents before
generating study notes.
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

    note_name, note_function = (
        _render_note_selector()
    )

    st.info(
        f"Selected Note Type : **{note_name}**"
    )

    st.markdown(
        "<br>",
        unsafe_allow_html=True,
    )

    _render_action_panel(
        selected_document,
        note_name,
        note_function,
    )

    st.markdown(
        "<br>",
        unsafe_allow_html=True,
    )

    _render_previous_notes()

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
# Sidebar Notes Statistics
# =============================================================================

def render_notes_sidebar() -> None:
    """
    Optional sidebar notes information.
    """

    notes = get_notes()

    if not notes:

        return

    st.sidebar.markdown("---")

    st.sidebar.markdown(
        "### 📚 Notes"
    )

    response = str(
        notes.get(
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
            notes.get(
                "citations",
                [],
            )
        ),
    )

    if st.sidebar.button(
        "🗑 Clear Notes",
        use_container_width=True,
    ):

        set_notes(
            {},
        )

        st.rerun()


# =============================================================================
# Notes Utilities
# =============================================================================

def export_notes() -> None:
    """
    Export notes text.
    """

    notes = get_notes()

    if not notes:

        return

    response = notes.get(
        "response",
        "",
    )

    st.download_button(

        label="📥 Export Notes",

        data=str(response),

        file_name="study_notes.txt",

        mime="text/plain",

        use_container_width=True,

    )


def notes_available() -> bool:
    """
    Check whether notes exist.
    """

    notes = get_notes()

    return bool(notes)
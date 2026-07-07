"""
File: frontend/components/upload_widget.py

Enterprise Upload Widget
"""

from __future__ import annotations

from pathlib import Path

import streamlit as st

from utils.constants import (
    MAX_FILE_SIZE_MB,
    MAX_UPLOAD_FILES,
    SUPPORTED_FILE_TYPES,
)

from utils.helpers import (
    file_icon,
    file_size,
    page_title,
)


# =============================================================================
# Helpers
# =============================================================================

def _is_duplicate(
    uploaded_files: list,
    filename: str,
) -> bool:
    """
    Check duplicate filename.
    """

    names = [

        file.name

        for file in uploaded_files

    ]

    return names.count(filename) > 1


def _validate_files(
    uploaded_files: list,
) -> tuple[bool, str]:
    """
    Validate uploaded files.
    """

    if not uploaded_files:

        return False, "Please select at least one document."

    if len(uploaded_files) > MAX_UPLOAD_FILES:

        return (

            False,

            f"Maximum {MAX_UPLOAD_FILES} files are allowed."

        )

    for file in uploaded_files:

        extension = Path(file.name).suffix.lower().replace(
            ".",
            "",
        )

        if extension not in SUPPORTED_FILE_TYPES:

            return (

                False,

                f"{file.name} is not supported."

            )

        size_mb = file.size / (1024 * 1024)

        if size_mb > MAX_FILE_SIZE_MB:

            return (

                False,

                f"{file.name} exceeds {MAX_FILE_SIZE_MB} MB."

            )

    return True, ""


# =============================================================================
# Upload Header
# =============================================================================

def _render_header() -> None:
    """
    Upload page heading.
    """

    page_title(

        "📤 Upload Documents",

        (
            "Upload PDF documents and images to build "
            "your RAG knowledge base."
        ),

    )


# =============================================================================
# Upload Area
# =============================================================================

def _render_uploader():
    """
    Drag & Drop uploader.
    """

    return st.file_uploader(

        label="Upload Documents",

        key="upload_widget",

        type=SUPPORTED_FILE_TYPES,

        accept_multiple_files=True,

        label_visibility="collapsed",

        help=(
            "Supported formats: "
            "PDF, PNG, JPG, JPEG, BMP, TIFF, WEBP"
        ),

    )


# =============================================================================
# Upload Summary
# =============================================================================

def _render_summary(
    uploaded_files: list,
) -> None:
    """
    Display upload summary.
    """

    pdf_count = 0

    image_count = 0

    total_size = 0

    for file in uploaded_files:

        total_size += file.size

        if file.name.lower().endswith(".pdf"):

            pdf_count += 1

        else:

            image_count += 1

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(

            "Files",

            len(uploaded_files),

        )

    with col2:

        st.metric(

            "PDF",

            pdf_count,

        )

    with col3:

        st.metric(

            "Images",

            image_count,

        )

    with col4:

        st.metric(

            "Size",

            file_size(total_size),

        )


# =============================================================================
# File Preview
# =============================================================================

def _render_file_preview(
    uploaded_files: list,
) -> None:
    """
    Display uploaded files.
    """

    st.markdown("### Selected Files")

    for file in uploaded_files:

        duplicate = _is_duplicate(

            uploaded_files,

            file.name,

        )

        badge = (

            " 🔴 Duplicate"

            if duplicate

            else ""

        )

        st.markdown(

            f"""

<div class="file-card">

<div class="file-left">

<div class="file-icon">

{file_icon(file.name)}

</div>

<div class="file-details">

<div class="file-name">

{file.name}{badge}

</div>

<div class="file-meta">

{file_size(file.size)}

</div>

</div>

</div>

</div>

""",

            unsafe_allow_html=True,

        )

# =============================================================================
# Empty State
# =============================================================================

def _render_empty_state() -> None:
    """
    Display empty upload state.
    """

    st.markdown(
        """
<div class="empty-state">

<div class="empty-icon">
📂
</div>

<h3>No Documents Selected</h3>

<p>

Drag & Drop your research papers or images
to start building your knowledge base.

</p>

</div>
""",
        unsafe_allow_html=True,
    )


# =============================================================================
# Upload Actions
# =============================================================================

def _render_actions() -> bool:
    """
    Render upload buttons.

    Returns
    -------
    bool
        True if upload button pressed.
    """

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns([2, 8])

    upload = False

    with col1:

        upload = st.button(

            "🚀 Upload",

            type="primary",

            use_container_width=True,

        )

    with col2:

        if st.button(

            "🗑 Clear Selection",

            use_container_width=True,

        ):

            st.session_state.pop("uploaded_files", None)
            st.rerun()

    return upload


# =============================================================================
# Upload Progress
# =============================================================================

def render_progress(
    progress: int,
    message: str = "Uploading documents...",
) -> None:
    """
    Display upload progress.
    """

    progress = max(
        0,
        min(progress, 100),
    )

    st.markdown(
        f"""
<div class="progress-card">

<div class="progress-text">

{message}

</div>

</div>
""",
        unsafe_allow_html=True,
    )

    st.progress(progress / 100)


# =============================================================================
# Upload Widget
# =============================================================================

def render_upload_widget() -> tuple[bool, list]:
    """
    Enterprise upload widget.

    Returns
    -------
    tuple

    (
        upload_pressed,
        uploaded_files
    )
    """


    uploaded_files = _render_uploader()

    if not uploaded_files:

        _render_empty_state()

        return False, []

    valid, message = _validate_files(
        uploaded_files,
    )

    if not valid:

        st.error(message)

        return False, []

    _render_summary(
        uploaded_files,
    )

    st.markdown(
        "<br>",
        unsafe_allow_html=True,
    )

    _render_file_preview(
        uploaded_files,
    )

    upload_pressed = _render_actions()

    return (

        upload_pressed,

        uploaded_files,

    )
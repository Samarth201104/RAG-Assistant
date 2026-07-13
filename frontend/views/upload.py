"""
File: frontend/pages/upload.py

Enterprise Upload Page
"""

from __future__ import annotations

import streamlit as st

from components.loading import (
    loading_context,
    loading_success,
    loading_error,
)

from components.upload_widget import (
    render_upload_widget,
)

from services.api_client import (
    api_client,
)

from utils.helpers import (
    page_title,
    markdown_card,
)

from utils.session import (
    set_success,
    set_error,
)


# =============================================================================
# Refresh Collection
# =============================================================================

def _collection() -> dict:
    """
    Load collection information from backend.
    """

    return api_client.collection_summary()


# =============================================================================
# Upload PDFs
# =============================================================================

def _upload_pdfs(
    pdf_files: list,
) -> bool:
    """
    Upload PDF documents.
    """

    try:

        with loading_context(
            "Uploading PDF documents..."
        ):

            response = api_client.upload_pdf(
                pdf_files,
            )

        if response["success"]:

            loading_success(
                response["message"],
            )

            set_success(
                response["message"],
            )

            return True

        loading_error(
            response["message"],
        )

        set_error(
            response["message"],
        )

        return False

    except Exception as error:

        loading_error(
            str(error),
        )

        set_error(
            str(error),
        )

        return False


# =============================================================================
# Upload Images
# =============================================================================

def _upload_images(
    image_files: list,
) -> bool:
    """
    Upload image documents.
    """

    try:

        with loading_context(
            "Uploading images..."
        ):

            response = api_client.upload_images(
                image_files,
            )

        if response["success"]:

            loading_success(
                response["message"],
            )

            return True

        loading_error(
            response["message"],
        )

        return False

    except Exception as error:

        loading_error(
            str(error),
        )

        return False


# =============================================================================
# Upload Handler
# =============================================================================

def _handle_upload(
    uploaded_files: list,
) -> bool:
    """
    Upload selected files.
    """

    pdfs = []

    images = []

    for file in uploaded_files:

        if file.name.lower().endswith(
            ".pdf"
        ):

            pdfs.append(
                file,
            )

        else:

            images.append(
                file,
            )

    success = True

    if pdfs:

        success &= _upload_pdfs(
            pdfs,
        )

    if images:

        success &= _upload_images(
            images,
        )

    return success


# =============================================================================
# Collection Statistics
# =============================================================================

def _render_collection_statistics(
    summary: dict,
) -> None:
    """
    Render collection statistics.
    """

    documents = summary.get(
        "documents",
        [],
    )

    statistics = summary.get(
        "statistics",
        {},
    )

    total_documents = summary.get(
        "document_count",
        len(documents),
    )

    total_chunks = statistics.get(
        "total_chunks",
        0,
    )

    pdf_count = sum(

        1

        for document in documents

        if str(document).lower().endswith(
            ".pdf"
        )

    )

    image_count = (
        total_documents - pdf_count
    )

    st.markdown(
        "## 📊 Collection Statistics"
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "📄 Documents",
            total_documents,
        )

    with col2:

        st.metric(
            "🧩 Chunks",
            total_chunks,
        )

    with col3:

        st.metric(
            "📚 PDFs",
            pdf_count,
        )

    with col4:

        st.metric(
            "🖼 Images",
            image_count,
        )


# =============================================================================
# Knowledge Base
# =============================================================================

def _render_collection_summary() -> None:
    """
    Knowledge base overview.
    """

    markdown_card(
        """
<div class="dashboard-card">

<h3>

📚 Knowledge Base

</h3>

<p>

Upload PDFs and Images to build your
semantic knowledge base.

Every uploaded document is processed,
embedded and indexed inside ChromaDB
for Retrieval-Augmented Generation.

</p>

</div>
"""
    )

# =============================================================================
# Indexed Documents
# =============================================================================

def _render_documents(
    documents: list,
) -> None:
    """
    Render indexed documents.
    """

    st.markdown(
        "## 📚 Indexed Documents"
    )

    if not documents:

        st.info(
            "No indexed documents found. Upload a PDF or image to begin."
        )

        return

    for document in documents:

        if isinstance(
            document,
            dict,
        ):

            filename = document.get(
                "filename",
                "Unknown",
            )

        else:

            filename = str(
                document,
            )

        col1, col2 = st.columns(
            [10, 1]
        )

        with col1:

            markdown_card(
                f"""
<div class="file-card">

<div class="file-left">

<div class="file-icon">

📄

</div>

<div class="file-details">

<div class="file-name">

{filename}

</div>

<div class="file-meta">

Indexed in ChromaDB

</div>

</div>

</div>

</div>
"""
            )

        with col2:

            if st.button(

                "🗑",

                key=f"delete_{filename}",

                help="Delete document",

            ):

                with loading_context(
                    "Deleting document..."
                ):

                    response = api_client.delete_document(
                        filename,
                    )

                if response["success"]:

                    loading_success(
                        response["message"],
                    )

                    st.cache_data.clear()

                    st.rerun()

                else:

                    loading_error(
                        response["message"],
                    )


# =============================================================================
# Upload Page
# =============================================================================

def render_upload_page() -> None:
    """
    Enterprise upload page.
    """

    page_title(

        "📤 Upload Documents",

        (
            "Upload PDF documents and images "
            "to build your AI knowledge base."
        ),

    )

    upload_pressed, uploaded_files = (
        render_upload_widget()
    )

    if upload_pressed:

        if not uploaded_files:

            st.warning(
                "Please select at least one file."
            )

        else:

            success = _handle_upload(
                uploaded_files,
            )

            if success:

                st.cache_data.clear()

                st.toast(

                    "Documents uploaded successfully.",

                    icon="✅",

                )

                st.rerun()

    st.markdown(
        "<br>",
        unsafe_allow_html=True,
    )

    summary = _collection()

    _render_collection_statistics(
        summary,
    )

    st.markdown(
        "<br>",
        unsafe_allow_html=True,
    )

    _render_collection_summary()

    st.markdown(
        "<br>",
        unsafe_allow_html=True,
    )

    _render_documents(
        summary.get(
            "documents",
            [],
        )
    )
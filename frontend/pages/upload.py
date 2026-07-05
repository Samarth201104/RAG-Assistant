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
    update_dashboard,
    set_success,
    set_error,
)


# =============================================================================
# Refresh Dashboard Statistics
# =============================================================================

def _refresh_statistics() -> tuple[int, int]:
    """
    Refresh collection statistics.

    Returns
    -------
    tuple
        (document_count, chunk_count)
    """

    try:

        documents = api_client.list_documents()

        statistics = api_client.vector_statistics()

        document_count = len(documents)

        chunk_count = statistics.get(
            "total_chunks",
            0,
        )

        backend = (
            "Online"
            if api_client.backend_available()
            else "Offline"
        )

        update_dashboard(
            backend_status=backend,
            document_count=document_count,
            chunk_count=chunk_count,
        )

        return (

            document_count,

            chunk_count,

        )

    except Exception:

        return (0, 0)


# =============================================================================
# Upload PDFs
# =============================================================================

def _upload_pdfs(
    pdf_files: list,
) -> bool:
    """
    Upload PDF documents.
    """

    with loading_context(
        "Uploading PDF documents..."
    ):

        response = api_client.upload_pdf(
            pdf_files,
        )

    if response.get(
        "success",
        False,
    ):

        loading_success(

            response.get(
                "message",
                "Documents uploaded successfully.",
            )

        )

        set_success(

            response.get(
                "message",
                "Documents uploaded successfully.",
            )

        )

        _refresh_statistics()

        return True

    loading_error(

        response.get(
            "message",
            "Upload failed.",
        )

    )

    set_error(

        response.get(
            "message",
            "Upload failed.",
        )

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

    with loading_context(
        "Uploading images..."
    ):

        response = api_client.upload_images(
            image_files,
        )

    if response.get(
        "success",
        False,
    ):

        loading_success(

            response.get(
                "message",
                "Images uploaded successfully.",
            )

        )

        _refresh_statistics()

        return True

    loading_error(

        response.get(
            "message",
            "Image upload failed.",
        )

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

    pdf_files = []

    image_files = []

    for file in uploaded_files:

        if file.name.lower().endswith(".pdf"):

            pdf_files.append(file)

        else:

            image_files.append(file)

    success = True

    if pdf_files:

        success &= _upload_pdfs(
            pdf_files,
        )

    if image_files:

        success &= _upload_images(
            image_files,
        )

    return success


# =============================================================================
# Collection Statistics
# =============================================================================

def _render_collection_statistics() -> None:
    """
    Render collection statistics.
    """

    documents = api_client.list_documents()

    _render_collection_statistics(documents)

    _render_documents(documents)

    statistics = api_client.vector_statistics()

    total_documents = len(documents)

    total_chunks = statistics.get(
        "total_chunks",
        0,
    )

    pdf_count = sum(

        1

        for document in documents

        if str(document).lower().endswith(".pdf")

    )

    image_count = total_documents - pdf_count

    total_size = statistics.get(
        "collection_size",
        "N/A",
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

    st.caption(
        f"Storage Usage : {total_size}"
    )


# =============================================================================
# Upload Summary Card
# =============================================================================

def _render_collection_summary() -> None:
    """
    Render collection summary.
    """

    markdown_card(
        """
<div class="dashboard-card">

<h3>

📚 Knowledge Base

</h3>

<p>

Upload research papers and images to
build your AI knowledge base.

Every uploaded document is indexed
inside ChromaDB and becomes searchable
using semantic retrieval.

</p>

</div>
"""
    )

# =============================================================================
# Indexed Documents
# =============================================================================

def _render_documents() -> None:
    """
    Display indexed documents.
    """

    st.markdown("## 📚 Indexed Documents")

    try:

        documents = api_client.list_documents()

        _render_collection_statistics(documents)

        _render_documents(documents)

        if not documents:

            st.info(
                "No indexed documents found."
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

                filename = str(document)

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

                    help="Delete Document",

                ):

                    with loading_context(
                        "Deleting document..."
                    ):

                        response = api_client.delete_document(
                            filename,
                        )

                    if response.get(
                        "success",
                        False,
                    ):

                        loading_success(

                            response.get(
                                "message",
                                "Document deleted.",
                            )

                        )

                        _refresh_statistics()

                        st.cache_data.clear()

                        st.rerun()

                    else:

                        loading_error(

                            response.get(
                                "message",
                                "Delete failed.",
                            )

                        )

    except Exception as error:

        loading_error(
            str(error),
        )


# =============================================================================
# Upload Page
# =============================================================================

def render_upload_page() -> None:
    """
    Render upload page.
    """

    page_title(

        "📤 Upload Documents",

        "Upload research papers and images to build your knowledge base.",

    )

    upload_pressed, uploaded_files = (
        render_upload_widget()
    )

    if upload_pressed:

        if not uploaded_files:

            st.warning(
                "Please select one or more files."
            )

        else:

            success = _handle_upload(
                uploaded_files,
            )

            if success:

                st.cache_data.clear()

                st.toast(

                    "Upload completed successfully.",

                    icon="✅",

                )

                st.rerun()

    st.markdown(
        "<br>",
        unsafe_allow_html=True,
    )

    _render_collection_statistics()

    st.markdown(
        "<br>",
        unsafe_allow_html=True,
    )

    _render_collection_summary()

    st.markdown(
        "<br>",
        unsafe_allow_html=True,
    )

    _render_documents()
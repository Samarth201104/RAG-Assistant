"""
File: backend/api/upload.py
"""

from typing import Annotated

from fastapi import (
    APIRouter,
    File,
    HTTPException,
    UploadFile,
)

from core.logger import logger
from models.response_models import GenericResponse
from services.document_service import document_service

router = APIRouter(
    prefix="/upload",
    tags=["Upload"],
)


# ============================================================================
# Upload PDF(s)
# ============================================================================

@router.post(
    "/pdf",
    response_model=GenericResponse,
)
async def upload_pdfs(
    files: Annotated[list[UploadFile], File(...)],
):
    """
    Upload one or more PDF documents.
    """

    uploaded_files = []

    total_chunks = 0

    try:

        for file in files:

            documents = await document_service.process_pdf(
                file
            )

            uploaded_files.append(file.filename)

            total_chunks += len(documents)

        logger.info(
            f"{len(uploaded_files)} PDF(s) uploaded successfully."
        )

        return GenericResponse(
            success=True,
            message="PDF(s) uploaded successfully.",
            data={
                "uploaded_files": uploaded_files,
                "documents_uploaded": len(
                    uploaded_files
                ),
                "chunks_created": total_chunks,
                "vector_documents": document_service.list_vector_documents(),
                "statistics": document_service.vector_statistics(),
            },
        )

    except Exception as error:

        logger.exception(error)

        raise HTTPException(
            status_code=500,
            detail=str(error),
        )


# ============================================================================
# Upload Image(s)
# ============================================================================

@router.post(
    "/image",
    response_model=GenericResponse,
)
async def upload_images(
    files: Annotated[list[UploadFile], File(...)],
):
    """
    Upload one or more images.
    """

    uploaded_files = []

    total_chunks = 0

    try:

        for file in files:

            documents = (
                await document_service.process_image(
                    file
                )
            )

            uploaded_files.append(
                file.filename
            )

            total_chunks += len(
                documents
            )

        logger.info(
            f"{len(uploaded_files)} image(s) uploaded successfully."
        )

        return GenericResponse(
            success=True,
            message="Image(s) uploaded successfully.",
            data={
                "uploaded_files": uploaded_files,
                "documents_uploaded": len(
                    uploaded_files
                ),
                "chunks_created": total_chunks,
                "vector_documents": document_service.list_vector_documents(),
                "statistics": document_service.vector_statistics(),
            },
        )

    except Exception as error:

        logger.exception(error)

        raise HTTPException(
            status_code=500,
            detail=str(error),
        )


# ============================================================================
# Uploaded PDFs
# ============================================================================

@router.get(
    "/pdfs",
    response_model=GenericResponse,
)
async def list_uploaded_pdfs():
    """
    List uploaded PDF documents.
    """

    return GenericResponse(
        success=True,
        message="Uploaded PDFs.",
        data={
            "documents": document_service.list_uploaded_pdfs(),
        },
    )


# ============================================================================
# Uploaded Images
# ============================================================================

@router.get(
    "/images",
    response_model=GenericResponse,
)
async def list_uploaded_images():
    """
    List uploaded images.
    """

    return GenericResponse(
        success=True,
        message="Uploaded Images.",
        data={
            "images": document_service.list_uploaded_images(),
        },
    )


# ============================================================================
# Vector Database Documents
# ============================================================================

@router.get(
    "/documents",
    response_model=GenericResponse,
)
async def list_vector_documents():
    """
    List documents stored in ChromaDB.
    """

    return GenericResponse(
        success=True,
        message="Indexed documents.",
        data={
            "documents": document_service.list_vector_documents(),
        },
    )


# ============================================================================
# Delete Document
# ============================================================================

@router.delete(
    "/document/{filename}",
    response_model=GenericResponse,
)
async def delete_document(
    filename: str,
):
    """
    Delete a document from ChromaDB.
    """

    try:

        document_service.delete_vector_document(
            filename
        )

        return GenericResponse(
            success=True,
            message=f"{filename} deleted successfully.",
            data={
                "remaining_documents": document_service.list_vector_documents(),
            },
        )

    except Exception as error:

        logger.exception(error)

        raise HTTPException(
            status_code=500,
            detail=str(error),
        )


# ============================================================================
# Vector Database Statistics
# ============================================================================

@router.get(
    "/statistics",
    response_model=GenericResponse,
)
async def vector_statistics():
    """
    Returns ChromaDB statistics.
    """

    return GenericResponse(
        success=True,
        message="Vector database statistics.",
        data=document_service.vector_statistics(),
    )
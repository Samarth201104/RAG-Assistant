"""
File: backend/api/query.py
"""

from fastapi import APIRouter, HTTPException

from core.logger import logger
from models.request_models import (
    QueryRequest,
    SearchDocumentRequest,
)
from models.response_models import AIResponse
from services.rag_service import rag_service

router = APIRouter(
    prefix="/query",
    tags=["RAG Chat"],
)


# ============================================================================
# Chat with all uploaded documents
# ============================================================================

@router.post(
    "",
    response_model=AIResponse,
)
async def query_documents(
    request: QueryRequest,
):
    """
    Query all indexed documents.
    """

    try:

        logger.info(
            f"Received query: {request.question}"
        )

        response = rag_service.query(
            question=request.question,
            top_k=request.top_k,
        )

        return AIResponse(
            success=True,
            message="Answer generated successfully.",
            response=response,
        )

    except Exception as error:

        logger.exception(error)

        raise HTTPException(
            status_code=500,
            detail=str(error),
        )


# ============================================================================
# Search inside a specific uploaded document
# ============================================================================

@router.post(
    "/document",
    response_model=AIResponse,
)
async def query_single_document(
    request: SearchDocumentRequest,
):
    """
    Query a single uploaded document.
    """

    try:

        logger.info(
            f"Searching inside document: {request.filename}"
        )

        response = rag_service.query_document(
            filename=request.filename,
            question=request.question,
            top_k=request.top_k,
        )

        return AIResponse(
            success=True,
            message="Answer generated successfully.",
            response=response,
        )

    except Exception as error:

        logger.exception(error)

        raise HTTPException(
            status_code=500,
            detail=str(error),
        )


# ============================================================================
# Retrieve Chunks Only (Debug Endpoint)
# ============================================================================

@router.post(
    "/retrieve",
    response_model=AIResponse,
)
async def retrieve_chunks(
    request: QueryRequest,
):
    """
    Retrieve relevant chunks without generating an answer.

    Useful for debugging retrieval quality.
    """

    try:

        documents = rag_service.retrieve_only(
            question=request.question,
            top_k=request.top_k,
        )

        chunks = []

        for document in documents:

            chunks.append(
                {
                    "content": document.page_content,
                    "metadata": document.metadata,
                }
            )

        return AIResponse(
            success=True,
            message="Retrieved relevant chunks.",
            response={
                "query": request.question,
                "retrieved_chunks": len(chunks),
                "documents": chunks,
            },
        )

    except Exception as error:

        logger.exception(error)

        raise HTTPException(
            status_code=500,
            detail=str(error),
        )


# ============================================================================
# RAG Service Health
# ============================================================================

@router.get(
    "/health",
)
async def rag_health():
    """
    Health check for RAG service.
    """

    return rag_service.health_check()
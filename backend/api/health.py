"""
File: backend/api/health.py
"""

from fastapi import APIRouter

from core.config import settings
from models.response_models import HealthResponse
from services.rag_service import rag_service
from services.summarization_service import (
    summarization_service,
)
from vectorstore.chroma_manager import chroma_manager

router = APIRouter(
    prefix="/health",
    tags=["Health"],
)


# ---------------------------------------------------------------------------

@router.get(
    "",
    response_model=HealthResponse,
)
async def health():
    """
    Basic API Health Check.
    """

    return HealthResponse(
        status="Healthy",
        service="MultiModal RAG Research Assistant",
        version="1.0.0",
    )


# ---------------------------------------------------------------------------

@router.get(
    "/rag",
)
async def rag_health():
    """
    RAG Service Health.
    """

    return rag_service.health_check()


# ---------------------------------------------------------------------------

@router.get(
    "/summarization",
)
async def summarization_health():
    """
    Summarization Service Health.
    """

    return summarization_service.health_check()


# ---------------------------------------------------------------------------

@router.get(
    "/vectordb",
)
async def vectordb_health():
    """
    ChromaDB Health.
    """

    return chroma_manager.get_collection_statistics()


# ---------------------------------------------------------------------------

@router.get(
    "/config",
)
async def configuration():
    """
    Current Application Configuration.
    """

    return {
        "gemini_model": settings.GEMINI_MODEL,
        "embedding_model": settings.EMBEDDING_MODEL,
        "chunk_size": settings.CHUNK_SIZE,
        "chunk_overlap": settings.CHUNK_OVERLAP,
        "top_k": settings.TOP_K,
        "vector_database": settings.CHROMA_DB_PATH,
    }


# ---------------------------------------------------------------------------

@router.get(
    "/ready",
)
async def readiness():
    """
    Readiness Probe.

    Useful for deployment and Docker.
    """

    return {
        "ready": True,
        "message": "Application is ready."
    }


# ---------------------------------------------------------------------------

@router.get(
    "/live",
)
async def liveness():
    """
    Liveness Probe.
    """

    return {
        "alive": True,
        "message": "Application is running."
    }
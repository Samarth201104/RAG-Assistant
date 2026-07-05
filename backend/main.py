"""
File: backend/main.py
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.compare import router as compare_router
from api.health import router as health_router
from api.notes import router as notes_router
from api.query import router as query_router
from api.summarize import router as summarize_router
from api.upload import router as upload_router

from core.config import settings
from core.logger import logger


# =============================================================================
# Application Lifecycle
# =============================================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application startup and shutdown events.
    """

    logger.info("=" * 60)
    logger.info("Starting MultiModal RAG Research Assistant...")
    logger.info("=" * 60)

    logger.info(f"Gemini Model      : {settings.GEMINI_MODEL}")
    logger.info(f"Embedding Model   : {settings.EMBEDDING_MODEL}")
    logger.info(f"Vector DB         : {settings.CHROMA_DB_PATH}")
    logger.info(f"Chunk Size        : {settings.CHUNK_SIZE}")
    logger.info(f"Chunk Overlap     : {settings.CHUNK_OVERLAP}")
    logger.info(f"Top-K Retrieval   : {settings.TOP_K}")

    logger.info("Backend started successfully.")

    yield

    logger.info("=" * 60)
    logger.info("Stopping Backend...")
    logger.info("=" * 60)


# =============================================================================
# FastAPI Application
# =============================================================================

app = FastAPI(
    title="MultiModal RAG Research Assistant",
    description="""
A portfolio-quality Retrieval Augmented Generation (RAG) application
built using FastAPI, LangChain, ChromaDB and Gemini.

Features
---------
• PDF Processing
• Image OCR
• Semantic Search
• Research Paper Summarization
• Paper Comparison
• Study Notes Generation
• Source Citations
""",
    version="1.0.0",
    lifespan=lifespan,
)


# =============================================================================
# CORS
# =============================================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # Restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =============================================================================
# Register Routers
# =============================================================================

app.include_router(health_router)

app.include_router(upload_router)

app.include_router(query_router)

app.include_router(summarize_router)

app.include_router(compare_router)

app.include_router(notes_router)


# =============================================================================
# Root Endpoint
# =============================================================================

@app.get(
    "/",
    tags=["Root"],
)
async def root():
    """
    Root Endpoint.
    """

    return {

        "application": "MultiModal RAG Research Assistant",

        "version": "1.0.0",

        "status": "Running",

        "docs": "/docs",

        "redoc": "/redoc",

    }


# =============================================================================
# API Information
# =============================================================================

@app.get(
    "/api",
    tags=["Root"],
)
async def api_information():
    """
    API Information.
    """

    return {

        "upload": "/upload",

        "query": "/query",

        "summarize": "/summarize",

        "compare": "/compare",

        "notes": "/notes",

        "health": "/health",

    }
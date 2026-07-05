"""
FastAPI API Package

Registers all API routers.
"""

from .health import router as health_router
from .upload import router as upload_router
from .query import router as query_router
from .summarize import router as summarize_router
from .compare import router as compare_router
from .notes import router as notes_router

__all__ = [
    "health_router",
    "upload_router",
    "query_router",
    "summarize_router",
    "compare_router",
    "notes_router",
]
"""
File: backend/core/config.py

Purpose:
---------
Loads environment variables from the .env file and exposes them
through a Settings object.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

from core.constants import (
    DEFAULT_CHUNK_OVERLAP,
    DEFAULT_CHUNK_SIZE,
    DEFAULT_TOP_K,
)

# ----------------------------------------
# Locate Project Root
# ----------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

# Load .env
load_dotenv(BASE_DIR / ".env")


class Settings:
    """
    Centralized configuration class.

    Every module should import this object instead of
    calling os.getenv() repeatedly.
    """

    # ==========================
    # Gemini
    # ==========================

    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

    GEMINI_MODEL = os.getenv(
        "GEMINI_MODEL",
        "gemini-2.5-flash",
    )

    # ==========================
    # Embedding
    # ==========================

    EMBEDDING_MODEL = os.getenv(
        "EMBEDDING_MODEL",
        "sentence-transformers/all-MiniLM-L6-v2",
    )

    # ==========================
    # ChromaDB
    # ==========================

    CHROMA_DB_PATH = os.getenv(
        "CHROMA_DB_PATH",
        str(BASE_DIR / "vectordb"),
    )

    # ==========================
    # Chunking
    # ==========================

    CHUNK_SIZE = int(
        os.getenv(
            "CHUNK_SIZE",
            DEFAULT_CHUNK_SIZE,
        )
    )

    CHUNK_OVERLAP = int(
        os.getenv(
            "CHUNK_OVERLAP",
            DEFAULT_CHUNK_OVERLAP,
        )
    )

    # ==========================
    # Retrieval
    # ==========================

    TOP_K = int(
        os.getenv(
            "TOP_K",
            DEFAULT_TOP_K,
        )
    )

    # ==========================
    # Logging
    # ==========================

    LOG_LEVEL = os.getenv(
        "LOG_LEVEL",
        "INFO",
    )

    # ==========================
    # Upload Paths
    # ==========================

    UPLOAD_PDF_DIR = os.getenv(
        "UPLOAD_PDF_DIR",
        str(BASE_DIR / "data" / "uploads" / "pdfs"),
    )

    UPLOAD_IMAGE_DIR = os.getenv(
        "UPLOAD_IMAGE_DIR",
        str(BASE_DIR / "data" / "uploads" / "images"),
    )

    PROCESSED_DATA_DIR = os.getenv(
        "PROCESSED_DATA_DIR",
        str(BASE_DIR / "data" / "processed"),
    )

    TEMP_DIR = os.getenv(
        "TEMP_DIR",
        str(BASE_DIR / "data" / "temp"),
    )

    TEMPERATURE = float(
        os.getenv(
            "TEMPERATURE",
            0.2,
        )
    )

    MAX_OUTPUT_TOKENS = int(
        os.getenv(
            "MAX_OUTPUT_TOKENS",
            2048,
        )
    )


settings = Settings()

# =============================================================================
# Create Required Directories
# =============================================================================

Path(settings.CHROMA_DB_PATH).mkdir(
    parents=True,
    exist_ok=True,
)

Path(settings.UPLOAD_PDF_DIR).mkdir(
    parents=True,
    exist_ok=True,
)

Path(settings.UPLOAD_IMAGE_DIR).mkdir(
    parents=True,
    exist_ok=True,
)

Path(settings.PROCESSED_DATA_DIR).mkdir(
    parents=True,
    exist_ok=True,
)

Path(settings.TEMP_DIR).mkdir(
    parents=True,
    exist_ok=True,
)
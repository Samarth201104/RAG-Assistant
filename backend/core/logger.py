"""
File: backend/core/logger.py

Purpose
-------
Centralized logging configuration for the entire application.
"""

from __future__ import annotations

import logging
import os

from core.config import Settings
from core.constants import LOG_DIR, LOG_FORMAT


# =============================================================================
# Create Log Directory
# =============================================================================

os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(
    LOG_DIR,
    "application.log",
)


# =============================================================================
# Configure Root Logger
# =============================================================================

logging.basicConfig(
    level=getattr(
        logging,
        Settings.LOG_LEVEL.upper(),
    ),
    format=LOG_FORMAT,
    handlers=[
        logging.FileHandler(
            LOG_FILE,
            encoding="utf-8",
        ),
        logging.StreamHandler(),
    ],
    force=True,
)


# =============================================================================
# Reduce Third-Party Logging
# =============================================================================

QUIET_LOGGERS = [

    "httpx",
    "httpcore",
    "watchfiles",
    "watchfiles.main",
    "urllib3",
    "chromadb",
    "sentence_transformers",
    "transformers",
    "huggingface_hub",
    "easyocr",
    "PIL",
    "google_genai",

]

for name in QUIET_LOGGERS:

    logging.getLogger(name).setLevel(
        logging.WARNING,
    )


# =============================================================================
# Keep FastAPI/Uvicorn Request Logs
# =============================================================================

logging.getLogger("uvicorn").setLevel(
    logging.INFO,
)

logging.getLogger("uvicorn.access").setLevel(
    logging.INFO,
)

logging.getLogger("uvicorn.error").setLevel(
    logging.INFO,
)


# =============================================================================
# Application Logger
# =============================================================================

logger = logging.getLogger("RAG-System")

logger.setLevel(
    getattr(
        logging,
        Settings.LOG_LEVEL.upper(),
    )
)

logger.propagate = False

if not logger.handlers:

    formatter = logging.Formatter(
        LOG_FORMAT,
    )

    console_handler = logging.StreamHandler()

    console_handler.setFormatter(
        formatter,
    )

    file_handler = logging.FileHandler(
        LOG_FILE,
        encoding="utf-8",
    )

    file_handler.setFormatter(
        formatter,
    )

    logger.addHandler(
        console_handler,
    )

    logger.addHandler(
        file_handler,
    )
"""
File: backend/core/constants.py

Purpose:
---------
This file stores all application-wide constants.
Having constants in one place improves maintainability and avoids
hardcoding values throughout the project.
"""

# ==============================
# Application
# ==============================

APP_NAME = "MultiModal RAG Research Assistant"
APP_VERSION = "1.0.0"

# ==============================
# Chunking Configuration
# ==============================

DEFAULT_CHUNK_SIZE = 1000
DEFAULT_CHUNK_OVERLAP = 200

# ==============================
# Retrieval
# ==============================

DEFAULT_TOP_K = 5

# ==============================
# Supported File Formats
# ==============================

SUPPORTED_PDF_EXTENSIONS = [".pdf"]

SUPPORTED_IMAGE_EXTENSIONS = [
    ".png",
    ".jpg",
    ".jpeg",
    ".bmp",
    ".tiff",
]

# ==============================
# Upload Directories
# ==============================

UPLOAD_PDF_DIR = "data/uploads/pdfs"

UPLOAD_IMAGE_DIR = "data/uploads/images"

PROCESSED_DATA_DIR = "data/processed"

TEMP_DIR = "data/temp"

VECTOR_DB_DIR = "vectordb"

LOG_DIR = "logs"

# ==============================
# Metadata Keys
# ==============================

METADATA_SOURCE = "source"

METADATA_PAGE = "page"

METADATA_CHUNK = "chunk_id"

METADATA_TYPE = "document_type"

# ==============================
# OCR
# ==============================

OCR_LANGUAGE = ["en"]

# ==============================
# Logging
# ==============================

LOG_FORMAT = (
    "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)
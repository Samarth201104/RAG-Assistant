"""
File: frontend/utils/constants.py

Application Constants
"""

from __future__ import annotations

from pathlib import Path

# =============================================================================
# Application
# =============================================================================

APP_NAME = "MultiModal RAG Research Assistant"

APP_DESCRIPTION = (
    "Enterprise AI-powered Research Assistant using "
    "FastAPI, LangChain, Gemini and ChromaDB."
)

APP_VERSION = "1.0.0"

PAGE_TITLE = APP_NAME

PAGE_ICON = "🤖"

LAYOUT = "wide"

INITIAL_SIDEBAR_STATE = "expanded"

# =============================================================================
# Paths
# =============================================================================

BASE_DIR = Path(__file__).resolve().parent.parent

ASSETS_DIR = BASE_DIR / "assets"

LOGO_PATH = ASSETS_DIR / "logo.png"

CSS_PATH = ASSETS_DIR / "styles.css"

# =============================================================================
# Backend
# =============================================================================

BACKEND_URL = "http://127.0.0.1:8000"

API_TIMEOUT = 120

# =============================================================================
# API Endpoints
# =============================================================================

HEALTH_ENDPOINT = "/health"

UPLOAD_PDF_ENDPOINT = "/upload/pdf"

UPLOAD_IMAGE_ENDPOINT = "/upload/image"

LIST_DOCUMENTS_ENDPOINT = "/upload/documents"

DELETE_DOCUMENT_ENDPOINT = "/upload/document"

VECTOR_STATISTICS_ENDPOINT = "/upload/statistics"

QUERY_ENDPOINT = "/query"

SUMMARY_ENDPOINT = "/summarize"

COMPARE_ENDPOINT = "/compare"

NOTES_ENDPOINT = "/notes"

# =============================================================================
# Navigation
# =============================================================================

NAVIGATION = [
    {
        "title": "Upload",
        "icon": "📤",
    },
    {
        "title": "Chat",
        "icon": "💬",
    },
    {
        "title": "Summarize",
        "icon": "📝",
    },
    {
        "title": "Compare",
        "icon": "⚖️",
    },
    {
        "title": "Notes",
        "icon": "📚",
    },
]

DEFAULT_PAGE = "Upload"

# =============================================================================
# Upload
# =============================================================================

SUPPORTED_FILE_TYPES = [
    "pdf",
    "png",
    "jpg",
    "jpeg",
    "bmp",
    "tiff",
    "webp",
]

MAX_UPLOAD_FILES = 20

MAX_FILE_SIZE_MB = 100

# =============================================================================
# Models
# =============================================================================

LLM_MODEL = "Gemini"

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

VECTOR_DATABASE = "ChromaDB"

# =============================================================================
# Chat
# =============================================================================

USER_AVATAR = "👤"

AI_AVATAR = "🤖"

WELCOME_MESSAGE = """
👋 Welcome!

Upload one or more research papers or images.

You can:

• Chat with documents
• Generate summaries
• Compare papers
• Create study notes
• Retrieve citations
"""

CHAT_PLACEHOLDER = (
    "Ask anything about your uploaded documents..."
)

MAX_CHAT_HISTORY = 100

# =============================================================================
# Dashboard
# =============================================================================

STATUS_ONLINE = "🟢 Online"

STATUS_OFFLINE = "🔴 Offline"

STATUS_WARNING = "🟡 Warning"

# =============================================================================
# Theme
# =============================================================================

PRIMARY_COLOR = "#3B82F6"

SECONDARY_COLOR = "#8B5CF6"

SUCCESS_COLOR = "#10B981"

WARNING_COLOR = "#F59E0B"

ERROR_COLOR = "#EF4444"

BACKGROUND_COLOR = "#0F172A"

CARD_COLOR = "#1E293B"

TEXT_COLOR = "#F8FAFC"

SUBTEXT_COLOR = "#94A3B8"

# =============================================================================
# Loading Messages
# =============================================================================

LOADING_MESSAGES = [

    "Connecting to backend...",

    "Uploading documents...",

    "Processing files...",

    "Creating embeddings...",

    "Searching vector database...",

    "Generating response...",

    "Preparing citations...",

    "Generating summary...",

    "Comparing documents...",

    "Generating study notes...",

]

# =============================================================================
# Footer
# =============================================================================

FOOTER_TEXT = (
    "Built with FastAPI • LangChain • Gemini • "
    "ChromaDB • Streamlit"
)

TECH_STACK = [

    "FastAPI",

    "LangChain",

    "Gemini",

    "ChromaDB",

    "Streamlit",

]

# =============================================================================
# Refresh
# =============================================================================

HEALTH_REFRESH_INTERVAL = 5

STATISTICS_REFRESH_INTERVAL = 10

# =============================================================================
# Messages
# =============================================================================

UPLOAD_SUCCESS = "Document uploaded successfully."

DELETE_SUCCESS = "Document deleted successfully."

UPLOAD_ERROR = "Failed to upload document."

DELETE_ERROR = "Failed to delete document."

SERVER_OFFLINE = (
    "Backend server is offline."
)

# =============================================================================
# Misc
# =============================================================================

COPYRIGHT = "© 2026 MultiModal RAG Research Assistant"

AUTHOR = "Samarth More"

DEBUG = False
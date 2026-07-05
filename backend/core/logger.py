"""
File: backend/core/logger.py

Purpose:
---------
Creates a centralized logger for the entire application.
"""

import logging
import os

from core.config import Settings
from core.constants import LOG_DIR, LOG_FORMAT

# ----------------------------------------
# Create Logs Directory
# ----------------------------------------

os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, "application.log")

# ----------------------------------------
# Configure Logger
# ----------------------------------------

logging.basicConfig(
    level=getattr(logging, Settings.LOG_LEVEL.upper()),
    format=LOG_FORMAT,
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(),
    ],
)

logger = logging.getLogger("RAG-System")
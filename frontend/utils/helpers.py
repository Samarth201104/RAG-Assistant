"""
File: frontend/utils/helpers.py

Reusable Helper Functions
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import streamlit as st


# =============================================================================
# File Helpers
# =============================================================================

def file_size(size: int) -> str:
    """
    Convert bytes into a human-readable string.
    """

    units = ["B", "KB", "MB", "GB", "TB"]

    value = float(size)

    for unit in units:

        if value < 1024:

            return f"{value:.2f} {unit}"

        value /= 1024

    return f"{value:.2f} PB"


def file_icon(filename: str) -> str:
    """
    Return an icon based on file extension.
    """

    extension = Path(filename).suffix.lower()

    icons = {

        ".pdf": "📄",

        ".png": "🖼️",

        ".jpg": "🖼️",

        ".jpeg": "🖼️",

        ".bmp": "🖼️",

        ".tiff": "🖼️",

        ".webp": "🖼️",

        ".txt": "📃",

        ".docx": "📘",

        ".pptx": "📙",

        ".xlsx": "📗",

    }

    return icons.get(extension, "📁")


def file_extension(filename: str) -> str:
    """
    Return file extension.
    """

    return Path(filename).suffix.lower()


def is_pdf(filename: str) -> bool:
    """
    Check if file is PDF.
    """

    return file_extension(filename) == ".pdf"


def is_image(filename: str) -> bool:
    """
    Check if file is an image.
    """

    return file_extension(filename) in {

        ".png",

        ".jpg",

        ".jpeg",

        ".bmp",

        ".tiff",

        ".webp",

    }


# =============================================================================
# Markdown Helpers
# =============================================================================

def markdown_card(content: str) -> None:
    """
    Render HTML card.
    """

    st.markdown(

        content,

        unsafe_allow_html=True,

    )


def divider() -> None:
    """
    Render divider.
    """

    st.markdown(
        "<hr>",
        unsafe_allow_html=True,
    )


def spacer(height: int = 20) -> None:
    """
    Vertical spacing.
    """

    st.markdown(

        f"<div style='height:{height}px'></div>",

        unsafe_allow_html=True,

    )


# =============================================================================
# Status Helpers
# =============================================================================

def success_box(message: str) -> None:
    """
    Success message.
    """

    st.success(message)


def warning_box(message: str) -> None:
    """
    Warning message.
    """

    st.warning(message)


def error_box(message: str) -> None:
    """
    Error message.
    """

    st.error(message)


def info_box(message: str) -> None:
    """
    Information message.
    """

    st.info(message)


# =============================================================================
# Badge Helpers
# =============================================================================

def status_badge(status: str) -> str:
    """
    Return colored HTML badge.
    """

    status = status.lower()

    if status in {

        "online",

        "connected",

        "success",

    }:

        css = "status-online"

    elif status in {

        "warning",

        "pending",

    }:

        css = "status-warning"

    else:

        css = "status-offline"

    return f"""

<span class="{css}">

{status.title()}

</span>

"""


# =============================================================================
# Text Helpers
# =============================================================================

def truncate(
    text: str,
    max_length: int = 120,
) -> str:
    """
    Truncate long text.
    """

    if len(text) <= max_length:

        return text

    return text[: max_length - 3] + "..."


def safe_get(
    data: dict,
    key: str,
    default: Any = None,
) -> Any:
    """
    Safe dictionary lookup.
    """

    return data.get(key, default)


# =============================================================================
# Download Helpers
# =============================================================================

def download_button(
    label: str,
    data: str,
    filename: str,
) -> None:
    """
    Standard download button.
    """

    st.download_button(

        label=label,

        data=data,

        file_name=filename,

        use_container_width=True,

    )


# =============================================================================
# Page Helpers
# =============================================================================

def page_title(
    title: str,
    description: str = "",
) -> None:
    """
    Standard page heading.
    """

    st.markdown(

        f"""

# {title}

{description}

""",

        unsafe_allow_html=True,

    )


# =============================================================================
# Metrics
# =============================================================================

def metric_card(
    title: str,
    value: Any,
) -> None:
    """
    Render Streamlit metric.
    """

    st.metric(

        title,

        value,

    )


# =============================================================================
# JSON Viewer
# =============================================================================

def json_view(
    data: dict,
) -> None:
    """
    Pretty JSON.
    """

    st.json(data)
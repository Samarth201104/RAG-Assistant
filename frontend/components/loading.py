"""
File: frontend/components/loading.py

Enterprise Loading Components
"""

from __future__ import annotations

from contextlib import contextmanager

import streamlit as st


# =============================================================================
# Loading Spinner
# =============================================================================

def loading(
    message: str = "Processing...",
) -> None:
    """
    Display loading animation.
    """

    st.markdown(
        f"""
<div class="loading-container">

<div class="loading-spinner"></div>

<div class="loading-text">

{message}

</div>

</div>
""",
        unsafe_allow_html=True,
    )


# =============================================================================
# Success
# =============================================================================

def loading_success(
    message: str,
) -> None:
    """
    Display success message.
    """

    st.markdown(
        f"""
<div class="success-card">

<div class="success-icon">

✅

</div>

<div class="success-text">

{message}

</div>

</div>
""",
        unsafe_allow_html=True,
    )


# =============================================================================
# Error
# =============================================================================

def loading_error(
    message: str,
) -> None:
    """
    Display error message.
    """

    st.markdown(
        f"""
<div class="error-card">

<div class="error-icon">

❌

</div>

<div class="error-text">

{message}

</div>

</div>
""",
        unsafe_allow_html=True,
    )


# =============================================================================
# Warning
# =============================================================================

def loading_warning(
    message: str,
) -> None:
    """
    Display warning message.
    """

    st.markdown(
        f"""
<div class="warning-card">

<div class="warning-icon">

⚠️

</div>

<div class="warning-text">

{message}

</div>

</div>
""",
        unsafe_allow_html=True,
    )


# =============================================================================
# Information
# =============================================================================

def loading_info(
    message: str,
) -> None:
    """
    Display information message.
    """

    st.markdown(
        f"""
<div class="info-card">

<div class="info-icon">

ℹ️

</div>

<div class="info-text">

{message}

</div>

</div>
""",
        unsafe_allow_html=True,
    )


# =============================================================================
# Progress
# =============================================================================

def loading_progress(
    value: int,
    text: str = "Processing...",
):
    """
    Render progress bar.
    """

    progress = st.progress(0)

    progress.progress(value)

    st.caption(text)

    return progress


# =============================================================================
# Context Manager
# =============================================================================

@contextmanager
def loading_context(
    message: str = "Processing...",
):
    """
    Context manager for long running operations.

    Example
    -------
    with loading_context("Uploading document..."):
        api_client.upload_pdf(files)
    """

    spinner = st.spinner(message)

    spinner.__enter__()

    try:

        yield

    finally:

        spinner.__exit__(None, None, None)


# =============================================================================
# Skeleton Placeholder
# =============================================================================

def loading_placeholder(
    height: int = 120,
):
    """
    Display loading skeleton.
    """

    st.markdown(
        f"""
<div
class="loading-placeholder"
style="height:{height}px;">
</div>
""",
        unsafe_allow_html=True,
    )


# =============================================================================
# Typing Indicator
# =============================================================================

def typing_indicator():
    """
    ChatGPT-style typing indicator.
    """

    st.markdown(
        """
<div class="typing-indicator">

<span></span>

<span></span>

<span></span>

</div>
""",
        unsafe_allow_html=True,
    )
"""
File: frontend/components/citation_card.py

Enterprise Citation Card Component
"""

from __future__ import annotations

from typing import Any

import streamlit as st


# =============================================================================
# Confidence Badge
# =============================================================================

def _confidence_color(
    confidence: float | None,
) -> str:
    """
    Return badge color class based on confidence.
    """

    if confidence is None:
        return "confidence-medium"

    if confidence >= 0.85:
        return "confidence-high"

    if confidence >= 0.60:
        return "confidence-medium"

    return "confidence-low"


# =============================================================================
# Citation Card
# =============================================================================

def render_citation_card(
    source: str,
    page: int | str,
    chunk: int | str,
    preview: str = "",
    confidence: float | None = None,
) -> None:
    """
    Render a single citation card.
    """

    confidence_text = (
        f"{confidence:.0%}"
        if confidence is not None
        else "N/A"
    )

    confidence_class = _confidence_color(
        confidence,
    )

    st.markdown(
        f"""
<div class="citation-card">

<div class="citation-header">

<div class="citation-title">

📄 {source}

</div>

<span class="citation-badge {confidence_class}">
{confidence_text}
</span>

</div>

<div class="citation-meta">

<span>📖 Page {page}</span>

<span>🧩 Chunk {chunk}</span>

</div>

</div>
""",
        unsafe_allow_html=True,
    )

    if preview:

        with st.expander(
            "👁 Source Preview",
            expanded=False,
        ):

            st.markdown(preview)


# =============================================================================
# Citation List
# =============================================================================

def render_citation_list(
    citations: list[dict[str, Any]],
) -> None:
    """
    Render all citations.
    """

    if not citations:

        st.info(
            "No citations available."
        )

        return

    st.markdown(
        "## 📚 References"
    )

    for citation in citations:

        render_citation_card(

            source=citation.get(
                "source",
                "Unknown",
            ),

            page=citation.get(
                "page",
                "-",
            ),

            chunk=citation.get(
                "chunk",
                "-",
            ),

            preview=citation.get(
                "preview",
                "",
            ),

            confidence=citation.get(
                "confidence",
                None,
            ),

        )


# =============================================================================
# Citation Statistics
# =============================================================================

def render_citation_statistics(
    citations: list[dict[str, Any]],
) -> None:
    """
    Display citation statistics.
    """

    if not citations:

        return

    unique_sources = {

        citation.get(
            "source",
            "Unknown",
        )

        for citation in citations

    }

    total_pages = {

        citation.get(
            "page",
            "-",
        )

        for citation in citations

    }

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "📄 Sources",
            len(unique_sources),
        )

    with col2:

        st.metric(
            "📚 Citations",
            len(citations),
        )

    with col3:

        st.metric(
            "📖 Pages",
            len(total_pages),
        )


# =============================================================================
# Complete Citation Section
# =============================================================================

def render_citation_section(
    citations: list[dict[str, Any]],
) -> None:
    """
    Render complete citation section.
    """

    if not citations:

        return

    st.markdown("---")

    render_citation_statistics(
        citations,
    )

    st.markdown("<br>", unsafe_allow_html=True)

    render_citation_list(
        citations,
    )
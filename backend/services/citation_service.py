"""
File: backend/services/citation_service.py

Citation Service

Responsibilities
----------------
1. Generate citations from retrieved chunks.
2. Remove duplicate citations.
3. Format citations for API responses.
4. Format citations for Streamlit UI.
"""

from typing import Dict, List

from langchain_core.documents import Document

from core.logger import logger


class CitationService:
    """
    Handles source citation generation.
    """

    # ------------------------------------------------------------------

    @staticmethod
    def generate_citations(
        documents: List[Document],
    ) -> List[Dict]:
        """
        Generate citations from retrieved documents.
        """

        citations = []

        seen = set()

        for document in documents:

            metadata = document.metadata

            citation = {
                "source": metadata.get(
                    "source",
                    "Unknown",
                ),
                "page": metadata.get(
                    "page",
                    "N/A",
                ),
                "chunk": metadata.get(
                    "chunk_index",
                    "N/A",
                ),
            }

            key = (
                citation["source"],
                citation["page"],
                citation["chunk"],
            )

            if key not in seen:
                seen.add(key)
                citations.append(citation)

        logger.info(
            f"Generated {len(citations)} citations."
        )

        return citations

    # ------------------------------------------------------------------

    @staticmethod
    def format_citations(
        citations: List[Dict],
    ) -> str:
        """
        Returns citations as formatted text.
        """

        if not citations:
            return "No citations available."

        lines = []

        for index, citation in enumerate(
            citations,
            start=1,
        ):

            lines.append(
                f"[{index}] "
                f"{citation['source']} "
                f"(Page {citation['page']}, "
                f"Chunk {citation['chunk']})"
            )

        return "\n".join(lines)

    # ------------------------------------------------------------------

    @staticmethod
    def markdown_citations(
        citations: List[Dict],
    ) -> str:
        """
        Markdown formatted citations for Streamlit.
        """

        if not citations:
            return ""

        markdown = "### Sources\n\n"

        for citation in citations:

            markdown += (
                f"- **{citation['source']}** "
                f"(Page {citation['page']}, "
                f"Chunk {citation['chunk']})\n"
            )

        return markdown

    # ------------------------------------------------------------------

    @staticmethod
    def api_response(
        answer: str,
        citations: List[Dict],
    ) -> Dict:
        """
        Standard API response.
        """

        return {
            "answer": answer,
            "citations": citations,
        }

    # ------------------------------------------------------------------

    @staticmethod
    def get_sources(
        documents: List[Document],
    ) -> List[str]:
        """
        Returns unique source filenames.
        """

        sources = set()

        for document in documents:

            source = document.metadata.get(
                "source",
                "Unknown",
            )

            sources.add(source)

        return sorted(list(sources))


citation_service = CitationService()

"""
File: backend/models/request_models.py
"""

from typing import Literal

from pydantic import BaseModel, Field


# ============================================================================
# RAG Chat
# ============================================================================

class QueryRequest(BaseModel):
    """
    Request model for RAG Chat.
    """

    question: str = Field(
        ...,
        min_length=1,
        description="User question."
    )

    top_k: int = Field(
        default=5,
        ge=1,
        le=20,
        description="Number of retrieved chunks."
    )


# ============================================================================
# Summarization
# ============================================================================

class SummarizeRequest(BaseModel):
    """
    Summarize one uploaded document.
    """

    filename: str = Field(
        ...,
        description="Uploaded PDF filename."
    )


# ============================================================================
# Compare Papers
# ============================================================================

class CompareRequest(BaseModel):
    """
    Compare two uploaded documents.
    """

    document_1: str = Field(
        ...,
        description="First uploaded document."
    )

    document_2: str = Field(
        ...,
        description="Second uploaded document."
    )


# ============================================================================
# Study Notes
# ============================================================================

class NotesRequest(BaseModel):
    """
    Generate study notes from one document.
    """

    filename: str = Field(
        ...,
        description="Uploaded PDF filename."
    )

    note_type: Literal[
        "short",
        "detailed",
        "flashcards",
        "interview",
        "mcq",
        "revision",
        "cheatsheet",
        "mindmap",
        "faq",
        "exam"
    ] = Field(
        default="detailed",
        description="Type of notes to generate."
    )


# ============================================================================
# Search Inside One Document
# ============================================================================

class SearchDocumentRequest(BaseModel):
    """
    Semantic search inside one document.
    """

    filename: str = Field(
        ...,
        description="Uploaded document filename."
    )

    question: str = Field(
        ...,
        min_length=1,
        description="Question."
    )

    top_k: int = Field(
        default=5,
        ge=1,
        le=20,
    )


# ============================================================================
# Delete Document
# ============================================================================

class DeleteDocumentRequest(BaseModel):
    """
    Delete a document from ChromaDB.
    """

    filename: str = Field(
        ...,
        description="Document filename."
    )
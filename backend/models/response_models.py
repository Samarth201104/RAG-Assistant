"""
File: backend/models/response_models.py
"""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class Citation(BaseModel):

    source: str

    page: int

    chunk: int


class QueryResponse(BaseModel):

    question: str

    answer: str

    citations: List[Citation]

    retrieved_chunks: int


class SummaryResponse(BaseModel):

    summary: str


class CompareResponse(BaseModel):

    comparison: str


class NotesResponse(BaseModel):

    notes: str


class UploadResponse(BaseModel):

    filename: str

    message: str

    chunks_created: int


class HealthResponse(BaseModel):

    status: str

    service: str

    version: str


class ErrorResponse(BaseModel):

    error: str

    detail: Optional[str] = None


class StatisticsResponse(BaseModel):

    total_documents: int

    total_chunks: int

    collection_name: str


class GenericResponse(BaseModel):

    success: bool

    message: str

    data: Optional[Dict[str, Any]] = Field(
        default_factory=dict
    )

class AIResponse(BaseModel):
    """
    Standard response model for all AI-generated outputs.
    """

    success: bool

    message: str

    response: Dict[str, Any]

    execution_time: Optional[float] = None
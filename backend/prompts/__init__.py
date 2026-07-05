"""
Prompt Package

Contains all prompt templates used by the
MultiModal RAG Research Assistant.
"""

from .rag_prompts import (
    RAG_SYSTEM_PROMPT,
    RAG_USER_PROMPT,
)

__all__ = [
    "RAG_SYSTEM_PROMPT",
    "RAG_USER_PROMPT",
]
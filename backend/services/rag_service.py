"""
File: backend/services/rag_service.py
"""

from typing import Dict, Optional

from core.config import settings
from core.logger import logger

from prompts.rag_prompts import (
    EMPTY_CONTEXT_PROMPT,
    RAG_SYSTEM_PROMPT,
    RAG_USER_PROMPT,
)

from services.citation_service import citation_service
from services.llm_service import llm_service
from services.retrieval_service import retrieval_service


class RAGService:
    """
    End-to-End Retrieval Augmented Generation Service.

    Workflow
    --------

    User Question
            │
            ▼
    Semantic Retrieval
            │
            ▼
    Relevant Chunks
            │
            ▼
    Prompt Construction
            │
            ▼
    Gemini
            │
            ▼
    Source Citations
            │
            ▼
    Final Response
    """

    def __init__(self):

        self.retriever = retrieval_service

        self.llm = llm_service

        self.citation = citation_service

    # ------------------------------------------------------------------

    def query(
        self,
        question: str,
        top_k: Optional[int] = None,
    ) -> Dict:
        """
        Main RAG Pipeline.
        """

        logger.info(
            f"Received Query : {question}"
        )

        if top_k is None:
            top_k = settings.TOP_K

        retrieved_documents = self.retriever.retrieve(
            query=question,
            top_k=top_k,
        )

        if len(retrieved_documents) == 0:

            logger.warning(
                "No relevant documents found."
            )

            answer = self.llm.invoke(
                RAG_SYSTEM_PROMPT,
                EMPTY_CONTEXT_PROMPT,
            )

            return {
                "question": question,
                "answer": answer,
                "citations": [],
                "retrieved_chunks": 0,
            }

        context = self.retriever.build_context(
            retrieved_documents
        )

        user_prompt = RAG_USER_PROMPT.format(
            context=context,
            question=question,
        )

        answer = self.llm.invoke(
            system_prompt=RAG_SYSTEM_PROMPT,
            user_prompt=user_prompt,
        )

        citations = (
            self.citation.generate_citations(
                retrieved_documents
            )
        )

        logger.info(
            "Answer generated successfully."
        )

        return {
            "question": question,
            "answer": answer,
            "citations": citations,
            "retrieved_chunks": len(
                retrieved_documents
            ),
        }

    # ------------------------------------------------------------------

    async def aquery(
        self,
        question: str,
        top_k: Optional[int] = None,
    ) -> Dict:
        """
        Async RAG Pipeline.
        """

        logger.info(
            f"Async Query : {question}"
        )

        if top_k is None:
            top_k = settings.TOP_K

        retrieved_documents = self.retriever.retrieve(
            query=question,
            top_k=top_k,
        )

        if len(retrieved_documents) == 0:

            answer = await self.llm.ainvoke(
                RAG_SYSTEM_PROMPT,
                EMPTY_CONTEXT_PROMPT,
            )

            return {
                "question": question,
                "answer": answer,
                "citations": [],
                "retrieved_chunks": 0,
            }

        context = self.retriever.build_context(
            retrieved_documents
        )

        user_prompt = RAG_USER_PROMPT.format(
            context=context,
            question=question,
        )

        answer = await self.llm.ainvoke(
            system_prompt=RAG_SYSTEM_PROMPT,
            user_prompt=user_prompt,
        )

        citations = (
            self.citation.generate_citations(
                retrieved_documents
            )
        )

        return {
            "question": question,
            "answer": answer,
            "citations": citations,
            "retrieved_chunks": len(
                retrieved_documents
            ),
        }

    # ------------------------------------------------------------------

    def query_document(
        self,
        filename: str,
        question: str,
        top_k: Optional[int] = None,
    ) -> Dict:
        """
        Ask question from one specific document.
        """

        logger.info(
            f"Searching inside : {filename}"
        )

        document_data = (
            self.retriever.search_document(
                query=question,
                filename=filename,
            )
        )

        documents = document_data["documents"]

        if len(documents) == 0:

            return {
                "question": question,
                "answer": "No relevant information found.",
                "citations": [],
                "retrieved_chunks": 0,
            }

        context = document_data["context"]

        user_prompt = RAG_USER_PROMPT.format(
            context=context,
            question=question,
        )

        answer = self.llm.invoke(
            RAG_SYSTEM_PROMPT,
            user_prompt,
        )

        citations = (
            self.citation.generate_citations(
                documents
            )
        )

        return {
            "question": question,
            "answer": answer,
            "citations": citations,
            "retrieved_chunks": len(
                documents
            ),
        }

    # ------------------------------------------------------------------

    def retrieve_only(
        self,
        question: str,
        top_k: Optional[int] = None,
    ):
        """
        Returns only retrieved documents.
        Useful for debugging.
        """

        if top_k is None:
            top_k = settings.TOP_K

        return self.retriever.retrieve(
            query=question,
            top_k=top_k,
        )

    # ------------------------------------------------------------------

    def health_check(self) -> Dict:
        """
        Service Health.
        """

        return {
            "service": "RAG Service",
            "model": self.llm.get_model_name(),
            "top_k": settings.TOP_K,
            "status": "Running",
        }


rag_service = RAGService()
"""
File: backend/services/retrieval_service.py
"""

from typing import Dict, List, Optional

from langchain_core.documents import Document

from core.config import settings
from core.logger import logger
from vectorstore.chroma_manager import chroma_manager


class RetrievalService:
    """
    Handles all retrieval operations.

    Used by:
    - RAG Chat (Semantic Search)
    - Summarization (Entire Document)
    - Comparison (Entire Document)
    - Notes Generation (Entire Document)
    """

    def __init__(self):

        self.vectorstore = chroma_manager

    # ------------------------------------------------------------------
    # Semantic Retrieval (For Chat)
    # ------------------------------------------------------------------

    def retrieve(
        self,
        query: str,
        top_k: Optional[int] = None,
    ) -> List[Document]:
        """
        Retrieve top-k relevant chunks.
        """

        if top_k is None:
            top_k = settings.TOP_K

        logger.info(
            f"Semantic Retrieval | Query='{query}' | Top-K={top_k}"
        )

        return self.vectorstore.similarity_search(
            query=query,
            k=top_k,
        )

    # ------------------------------------------------------------------
    # Semantic Retrieval with Scores
    # ------------------------------------------------------------------

    def retrieve_with_scores(
        self,
        query: str,
        top_k: Optional[int] = None,
    ) -> List[Dict]:
        """
        Retrieve chunks with similarity scores.
        """

        if top_k is None:
            top_k = settings.TOP_K

        results = self.vectorstore.similarity_search_with_score(
            query=query,
            k=top_k,
        )

        output = []

        for document, score in results:

            output.append(
                {
                    "document": document,
                    "content": document.page_content,
                    "metadata": document.metadata,
                    "score": float(score),
                }
            )

        logger.info(
            f"Retrieved {len(output)} scored chunks."
        )

        return output

    # ------------------------------------------------------------------
    # Retrieve Inside One Document (Semantic)
    # ------------------------------------------------------------------

    def retrieve_by_document(
        self,
        query: str,
        filename: str,
        top_k: Optional[int] = None,
    ) -> List[Document]:
        """
        Semantic retrieval inside one document.
        """

        if top_k is None:
            top_k = settings.TOP_K

        logger.info(
            f"Searching '{filename}'"
        )

        return self.vectorstore.vectorstore.similarity_search(
            query=query,
            k=top_k,
            filter={
                "source": filename,
            },
        )

    # ------------------------------------------------------------------
    # Entire Document Retrieval
    # ------------------------------------------------------------------

    def get_document(
        self,
        filename: str,
    ) -> List[Document]:
        """
        Load every chunk of a document.

        Used by:
        - Summarization
        - Comparison
        - Notes
        """

        return self.vectorstore.get_document_chunks(
            filename
        )

    # ------------------------------------------------------------------
    # Build LLM Context
    # ------------------------------------------------------------------

    def build_context(
        self,
        documents: List[Document],
    ) -> str:
        """
        Convert LangChain documents into one context string.
        """

        context = []

        for index, document in enumerate(
            documents,
            start=1,
        ):

            metadata = document.metadata

            context.append(
                f"""
==============================
Chunk {index}

Source : {metadata.get("source")}

Page : {metadata.get("page")}

Chunk : {metadata.get("chunk_index")}

Content

{document.page_content}
"""
            )

        return "\n".join(context)

    # ------------------------------------------------------------------
    # Entire Document Context
    # ------------------------------------------------------------------

    def get_document_context(
        self,
        filename: str,
    ) -> str:
        """
        Returns the entire document as LLM context.
        """

        documents = self.get_document(
            filename
        )

        return self.build_context(
            documents
        )

    # ------------------------------------------------------------------
    # Semantic Context
    # ------------------------------------------------------------------

    def retrieve_context(
        self,
        query: str,
        top_k: Optional[int] = None,
    ) -> str:
        """
        Context for RAG Chat.
        """

        documents = self.retrieve(
            query=query,
            top_k=top_k,
        )

        return self.build_context(
            documents
        )

    # ------------------------------------------------------------------
    # Semantic Context + Documents
    # ------------------------------------------------------------------

    def retrieve_context_with_sources(
        self,
        query: str,
        top_k: Optional[int] = None,
    ) -> Dict:

        documents = self.retrieve(
            query=query,
            top_k=top_k,
        )

        return {

            "context":
                self.build_context(
                    documents
                ),

            "documents":
                documents,

        }

    # ------------------------------------------------------------------
    # Extract Sources
    # ------------------------------------------------------------------

    @staticmethod
    def extract_sources(
        documents: List[Document],
    ) -> List[Dict]:

        sources = []

        for document in documents:

            metadata = document.metadata

            sources.append(
                {
                    "source":
                        metadata.get("source"),

                    "page":
                        metadata.get("page"),

                    "chunk":
                        metadata.get("chunk_index"),
                }
            )

        return sources

    # ------------------------------------------------------------------
    # Search Inside One Document
    # ------------------------------------------------------------------

    def search_document(
        self,
        query: str,
        filename: str,
        top_k: Optional[int] = None,
    ) -> Dict:
        """
        Semantic search inside a single document.
        """

        documents = self.retrieve_by_document(
            query=query,
            filename=filename,
            top_k=top_k,
        )

        return {

            "context":
                self.build_context(
                    documents
                ),

            "documents":
                documents,

            "sources":
                self.extract_sources(
                    documents
                ),

        }

    # ------------------------------------------------------------------
    # Retrieval Statistics
    # ------------------------------------------------------------------

    def retrieval_statistics(
        self,
        query: str,
    ) -> Dict:

        documents = self.retrieve(
            query
        )

        return {

            "query":
                query,

            "retrieved_chunks":
                len(documents),

            "documents":
                len(
                    {
                        doc.metadata.get(
                            "source"
                        )
                        for doc in documents
                    }
                ),

        }


retrieval_service = RetrievalService()
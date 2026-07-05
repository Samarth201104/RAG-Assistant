"""
File: backend/services/embedding_service.py

Embedding Service

Responsibilities
----------------
1. Load embedding model once
2. Generate embeddings for documents
3. Generate embeddings for queries
4. Support batch embedding
"""

from typing import List

from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings

from core.config import settings
from core.logger import logger


class EmbeddingService:
    """
    Singleton Embedding Service.

    Loads the embedding model only once during
    application startup.
    """

    _instance = None
    _embeddings = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(
                EmbeddingService,
                cls,
            ).__new__(cls)

        return cls._instance

    # ------------------------------------------------------------

    def __init__(self):

        if self._embeddings is None:

            logger.info(
                "Loading Embedding Model..."
            )

            self._embeddings = HuggingFaceEmbeddings(
                model_name=settings.EMBEDDING_MODEL,
                model_kwargs={
                    "device": "cpu",
                },
                encode_kwargs={
                    "normalize_embeddings": True,
                },
            )

            logger.info(
                f"Embedding model loaded : {settings.EMBEDDING_MODEL}"
            )

    # ------------------------------------------------------------

    @property
    def embedding_model(self):
        """
        Returns LangChain embedding object.
        """

        return self._embeddings

    # ------------------------------------------------------------

    def embed_documents(
        self,
        documents: List[Document],
    ) -> List[List[float]]:
        """
        Generate embeddings for LangChain Documents.
        """

        logger.info(
            f"Generating embeddings for {len(documents)} chunks."
        )

        texts = [
            document.page_content
            for document in documents
        ]

        embeddings = self._embeddings.embed_documents(
            texts
        )

        logger.info(
            "Document embeddings generated."
        )

        return embeddings

    # ------------------------------------------------------------

    def embed_texts(
        self,
        texts: List[str],
    ) -> List[List[float]]:
        """
        Generate embeddings for plain text.
        """

        logger.info(
            f"Embedding {len(texts)} texts."
        )

        return self._embeddings.embed_documents(
            texts
        )

    # ------------------------------------------------------------

    def embed_query(
        self,
        query: str,
    ) -> List[float]:
        """
        Generate embedding for user query.
        """

        logger.info(
            "Generating query embedding."
        )

        return self._embeddings.embed_query(
            query
        )

    # ------------------------------------------------------------

    def embedding_dimension(self) -> int:
        """
        Returns embedding dimension.
        """

        vector = self.embed_query(
            "Embedding Dimension"
        )

        return len(vector)

    # ------------------------------------------------------------

    def similarity(
        self,
        text1: str,
        text2: str,
    ) -> float:
        """
        Computes cosine similarity between
        two texts.

        Returns
        -------
        float
        """

        import numpy as np

        embedding1 = self.embed_query(
            text1
        )

        embedding2 = self.embed_query(
            text2
        )

        embedding1 = np.array(
            embedding1
        )

        embedding2 = np.array(
            embedding2
        )

        similarity = np.dot(
            embedding1,
            embedding2,
        )

        return float(similarity)

    # ------------------------------------------------------------

    def get_model_name(self) -> str:
        """
        Returns current embedding model.
        """

        return settings.EMBEDDING_MODEL

        # ------------------------------------------------------------

    def get_embedding_function(self):
        """
        Returns the LangChain embedding function.
        """

        return self._embeddings

embedding_service = EmbeddingService()

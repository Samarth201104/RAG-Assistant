"""
File: backend/services/embedding_service.py
"""

from typing import List

import numpy as np
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings

from core.config import settings
from core.logger import logger


class EmbeddingService:

    _instance = None

    def __new__(cls):

        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._embeddings = None

        return cls._instance

    # ------------------------------------------------------------

    def _load_model(self):

        if self._embeddings is None:

            logger.info("Loading Embedding Model...")

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

        self._load_model()

        return self._embeddings

    # ------------------------------------------------------------

    def get_embedding_function(self):

        self._load_model()

        return self._embeddings

    # ------------------------------------------------------------

    def embed_documents(
        self,
        documents: List[Document],
    ):

        self._load_model()

        texts = [doc.page_content for doc in documents]

        return self._embeddings.embed_documents(texts)

    # ------------------------------------------------------------

    def embed_texts(
        self,
        texts: List[str],
    ):

        self._load_model()

        return self._embeddings.embed_documents(texts)

    # ------------------------------------------------------------

    def embed_query(
        self,
        query: str,
    ):

        self._load_model()

        return self._embeddings.embed_query(query)

    # ------------------------------------------------------------

    def embedding_dimension(self):

        return len(self.embed_query("dimension"))

    # ------------------------------------------------------------

    def similarity(
        self,
        text1: str,
        text2: str,
    ):

        e1 = np.array(self.embed_query(text1))
        e2 = np.array(self.embed_query(text2))

        return float(np.dot(e1, e2))

    # ------------------------------------------------------------

    def get_model_name(self):

        return settings.EMBEDDING_MODEL


embedding_service = EmbeddingService()
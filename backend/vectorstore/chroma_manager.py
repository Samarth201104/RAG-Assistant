"""
File: backend/vectorstore/chroma_manager.py
"""

from typing import Dict, List

from langchain_chroma import Chroma
from langchain_core.documents import Document

from core.config import settings
from core.logger import logger
from services.embedding_service import embedding_service


class ChromaManager:

    COLLECTION_NAME = "multimodal_rag"

    _instance = None

    def __new__(cls):

        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.vectorstore = None

        return cls._instance

    # ------------------------------------------------------------

    def _initialize(self):

        if self.vectorstore is None:

            logger.info("Initializing ChromaDB...")

            self.vectorstore = Chroma(
                collection_name=self.COLLECTION_NAME,
                persist_directory=settings.CHROMA_DB_PATH,
                embedding_function=embedding_service.get_embedding_function(),
            )

            logger.info("ChromaDB initialized successfully.")

    # ------------------------------------------------------------

    def add_documents(self, documents: List[Document]):

        self._initialize()

        if documents:
            self.vectorstore.add_documents(documents)

    # ------------------------------------------------------------

    def similarity_search(self, query: str, k: int):

        self._initialize()

        return self.vectorstore.similarity_search(
            query=query,
            k=k,
        )

    # ------------------------------------------------------------

    def similarity_search_with_score(self, query: str, k: int):

        self._initialize()

        return self.vectorstore.similarity_search_with_score(
            query=query,
            k=k,
        )

    # ------------------------------------------------------------

    def get_document_chunks(self, filename: str):

        self._initialize()

        results = self.vectorstore.get(
            where={"source": filename},
            include=["documents", "metadatas"],
        )

        docs = []

        for text, metadata in zip(
            results.get("documents", []),
            results.get("metadatas", []),
        ):

            docs.append(
                Document(
                    page_content=text,
                    metadata=metadata,
                )
            )

        return docs

    # ------------------------------------------------------------

    def list_documents(self):

        self._initialize()

        results = self.vectorstore.get()

        names = set()

        for metadata in results.get("metadatas", []):

            if metadata:
                names.add(metadata.get("source", "Unknown"))

        return sorted(list(names))

    # ------------------------------------------------------------

    def delete_document(self, filename: str):

        self._initialize()

        ids = self.vectorstore.get(
            where={"source": filename}
        ).get("ids", [])

        if ids:
            self.vectorstore.delete(ids=ids)

    # ------------------------------------------------------------

    def document_exists(self, filename: str):

        self._initialize()

        return len(
            self.vectorstore.get(
                where={"source": filename}
            ).get("ids", [])
        ) > 0

    # ------------------------------------------------------------

    def total_chunks(self):

        self._initialize()

        return len(
            self.vectorstore.get().get("ids", [])
        )

    # ------------------------------------------------------------

    def clear_collection(self):

        self._initialize()

        ids = self.vectorstore.get().get("ids", [])

        if ids:
            self.vectorstore.delete(ids=ids)

    # ------------------------------------------------------------

    def get_collection_statistics(self) -> Dict:

        self._initialize()

        return {
            "collection_name": self.COLLECTION_NAME,
            "total_documents": len(self.list_documents()),
            "total_chunks": self.total_chunks(),
        }


chroma_manager = ChromaManager()
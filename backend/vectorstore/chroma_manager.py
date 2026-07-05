"""
File: backend/vectorstore/chroma_manager.py
"""

from typing import Dict, List, Optional

from langchain_chroma import Chroma
from langchain_core.documents import Document

from core.config import settings
from core.logger import logger
from services.embedding_service import embedding_service


class ChromaManager:
    """
    Chroma Vector Database Manager.
    """

    COLLECTION_NAME = "multimodal_rag"

    def __init__(self):

        logger.info("Initializing ChromaDB...")

        self.vectorstore = Chroma(
            collection_name=self.COLLECTION_NAME,
            persist_directory=settings.CHROMA_DB_PATH,
            embedding_function=embedding_service.get_embedding_function(),
        )

        logger.info("ChromaDB initialized successfully.")

    # ------------------------------------------------------------------

    def add_documents(
        self,
        documents: List[Document],
    ) -> None:
        """
        Store LangChain Documents.
        """

        if not documents:

            logger.warning(
                "No documents to store."
            )

            return

        self.vectorstore.add_documents(
            documents
        )

        logger.info(
            f"{len(documents)} chunks stored."
        )

    # ------------------------------------------------------------------

    def similarity_search(
        self,
        query: str,
        k: int,
    ) -> List[Document]:
        """
        Semantic Retrieval.
        """

        return self.vectorstore.similarity_search(
            query=query,
            k=k,
        )

    # ------------------------------------------------------------------

    def similarity_search_with_score(
        self,
        query: str,
        k: int,
    ):
        """
        Semantic Retrieval with similarity score.
        """

        return self.vectorstore.similarity_search_with_score(
            query=query,
            k=k,
        )

    # ------------------------------------------------------------------

    def get_document_chunks(
        self,
        filename: str,
    ) -> List[Document]:
        """
        Load every chunk belonging to one document.

        Used by:

        - Summarization
        - Comparison
        - Notes
        """

        logger.info(
            f"Loading all chunks of {filename}"
        )

        results = self.vectorstore.get(
            where={
                "source": filename
            },
            include=[
                "documents",
                "metadatas",
            ],
        )

        documents = []

        texts = results.get(
            "documents",
            [],
        )

        metadatas = results.get(
            "metadatas",
            [],
        )

        for text, metadata in zip(
            texts,
            metadatas,
        ):

            documents.append(

                Document(
                    page_content=text,
                    metadata=metadata,
                )

            )

        logger.info(
            f"{len(documents)} chunks loaded."
        )

        return documents

    # ------------------------------------------------------------------

    def list_documents(
        self,
    ) -> List[str]:
        """
        List all indexed documents.
        """

        results = self.vectorstore.get()

        filenames = set()

        for metadata in results.get(
            "metadatas",
            [],
        ):

            if metadata:

                filenames.add(
                    metadata.get(
                        "source",
                        "Unknown",
                    )
                )

        return sorted(
            list(filenames)
        )

    # ------------------------------------------------------------------

    def delete_document(
        self,
        filename: str,
    ) -> None:
        """
        Delete every chunk of one document.
        """

        results = self.vectorstore.get(
            where={
                "source": filename
            }
        )

        ids = results.get(
            "ids",
            [],
        )

        if ids:

            self.vectorstore.delete(
                ids=ids
            )

            logger.info(
                f"{filename} removed."
            )

        else:

            logger.warning(
                f"{filename} not found."
            )

    # ------------------------------------------------------------------

    def document_exists(
        self,
        filename: str,
    ) -> bool:

        results = self.vectorstore.get(
            where={
                "source": filename
            }
        )

        return len(
            results.get(
                "ids",
                [],
            )
        ) > 0

    # ------------------------------------------------------------------

    def total_chunks(
        self,
    ) -> int:

        return len(
            self.vectorstore.get().get(
                "ids",
                [],
            )
        )

    # ------------------------------------------------------------------

    def clear_collection(
        self,
    ):
        """
        Delete every vector.
        """

        ids = self.vectorstore.get().get(
            "ids",
            [],
        )

        if ids:

            self.vectorstore.delete(
                ids=ids
            )

            logger.warning(
                "Collection cleared."
            )

    # ------------------------------------------------------------------

    def get_collection_statistics(
        self,
    ) -> Dict:

        return {

            "collection_name":
                self.COLLECTION_NAME,

            "total_documents":
                len(
                    self.list_documents()
                ),

            "total_chunks":
                self.total_chunks(),

        }


chroma_manager = ChromaManager()
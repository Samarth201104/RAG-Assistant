"""
File: backend/utils/chunk_utils.py

Purpose
-------
Provides reusable text chunking utilities for the
MultiModal RAG Research Assistant.

Responsibilities
----------------
1. Split text into semantic chunks
2. Preserve document metadata
3. Generate unique chunk IDs
4. Return LangChain Document objects
"""

from typing import Dict, List
from uuid import uuid4

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from core.config import settings
from core.logger import logger


class ChunkManager:
    """
    Handles text chunking using LangChain's
    RecursiveCharacterTextSplitter.
    """

    def __init__(self) -> None:

        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP,
            separators=[
                "\n\n",
                "\n",
                ". ",
                " ",
                "",
            ],
        )

    # --------------------------------------------------

    def create_chunks(
        self,
        text: str,
        metadata: Dict,
    ) -> List[Document]:
        """
        Split text into semantic chunks.

        Parameters
        ----------
        text : str
            Cleaned text.

        metadata : Dict
            Metadata associated with the document.

        Returns
        -------
        List[Document]
        """

        raw_chunks = self.text_splitter.split_text(text)

        documents = []

        for index, chunk in enumerate(raw_chunks):

            chunk_metadata = metadata.copy()

            chunk_metadata["chunk_id"] = str(uuid4())

            chunk_metadata["chunk_index"] = index

            documents.append(
                Document(
                    page_content=chunk,
                    metadata=chunk_metadata,
                )
            )

        logger.info(
            f"Generated {len(documents)} chunks."
        )

        return documents

    # --------------------------------------------------

    def create_document_chunks(
        self,
        pages: List[Dict],
        filename: str,
    ) -> List[Document]:
        """
        Creates chunks from a page-wise extracted PDF.

        Parameters
        ----------
        pages : List[Dict]

        Example

        [
            {
                "page":1,
                "text":"...."
            },
            {
                "page":2,
                "text":"...."
            }
        ]

        filename : str

        Returns
        -------
        List[Document]
        """

        all_chunks = []

        for page in pages:

            metadata = {
                "source": filename,
                "page": page["page"],
                "document_type": "pdf",
            }

            page_chunks = self.create_chunks(
                page["text"],
                metadata,
            )

            all_chunks.extend(page_chunks)

        logger.info(
            f"{filename} split into {len(all_chunks)} chunks."
        )

        return all_chunks

    # --------------------------------------------------

    @staticmethod
    def chunk_statistics(
        documents: List[Document],
    ) -> Dict:
        """
        Returns useful statistics about generated chunks.
        """

        if not documents:

            return {
                "total_chunks": 0,
                "average_chunk_length": 0,
            }

        lengths = [
            len(doc.page_content)
            for doc in documents
        ]

        return {
            "total_chunks": len(documents),
            "average_chunk_length": round(
                sum(lengths) / len(lengths),
                2,
            ),
            "largest_chunk": max(lengths),
            "smallest_chunk": min(lengths),
        }


chunk_manager = ChunkManager()
"""
File: backend/services/pdf_service.py
"""

from pathlib import Path
from typing import Dict, List

import fitz  # PyMuPDF
from langchain_core.documents import Document

from core.logger import logger
from utils.chunk_utils import chunk_manager
from utils.text_utils import text_cleaner


class PDFService:
    """
    Service responsible for processing PDF documents.

    Workflow
    --------
    PDF
        ↓
    Open PDF
        ↓
    Extract Page-wise Text
        ↓
    Clean Text
        ↓
    Chunk Text
        ↓
    Return LangChain Documents
    """

    def __init__(self):
        pass

    # ------------------------------------------------------------------#

    def process_pdf(self, pdf_path: Path) -> List[Document]:
        """
        Complete PDF processing pipeline.

        Parameters
        ----------
        pdf_path : Path

        Returns
        -------
        List[Document]
        """

        logger.info(f"Processing PDF: {pdf_path.name}")

        pages = self.extract_pages(pdf_path)

        documents = chunk_manager.create_document_chunks(
            pages=pages,
            filename=pdf_path.name,
        )

        logger.info(
            f"{pdf_path.name} processed successfully."
        )

        return documents

    # ------------------------------------------------------------------#

    def extract_pages(
        self,
        pdf_path: Path,
    ) -> List[Dict]:
        """
        Extract page-wise text.

        Returns
        -------
        [
            {
                "page":1,
                "text":"..."
            }
        ]
        """

        document = fitz.open(pdf_path)

        pages: List[Dict] = []

        for page_number, page in enumerate(document, start=1):

            raw_text = page.get_text()

            cleaned_text = text_cleaner.clean_pdf_text(
                raw_text
            )

            if not text_cleaner.validate_text(
                cleaned_text
            ):
                continue

            pages.append(
                {
                    "page": page_number,
                    "text": cleaned_text,
                }
            )

        document.close()

        logger.info(
            f"Extracted {len(pages)} pages from {pdf_path.name}"
        )

        return pages

    # ------------------------------------------------------------------#

    def extract_metadata(
        self,
        pdf_path: Path,
    ) -> Dict:
        """
        Extract PDF metadata.
        """

        document = fitz.open(pdf_path)

        metadata = document.metadata

        page_count = document.page_count

        document.close()

        return {
            "filename": pdf_path.name,
            "filepath": str(pdf_path),
            "title": metadata.get("title", ""),
            "author": metadata.get("author", ""),
            "subject": metadata.get("subject", ""),
            "keywords": metadata.get("keywords", ""),
            "creator": metadata.get("creator", ""),
            "producer": metadata.get("producer", ""),
            "page_count": page_count,
        }

    # ------------------------------------------------------------------#

    def get_document_statistics(
        self,
        pdf_path: Path,
    ) -> Dict:
        """
        Returns useful PDF statistics.
        """

        pages = self.extract_pages(pdf_path)

        total_characters = sum(
            len(page["text"])
            for page in pages
        )

        return {
            "filename": pdf_path.name,
            "pages": len(pages),
            "characters": total_characters,
        }

    # ------------------------------------------------------------------#

    def extract_page(
        self,
        pdf_path: Path,
        page_number: int,
    ) -> str:
        """
        Extract text from a single page.
        """

        document = fitz.open(pdf_path)

        if page_number < 1 or page_number > document.page_count:
            document.close()
            raise ValueError("Invalid page number.")

        page = document.load_page(page_number - 1)

        text = page.get_text()

        document.close()

        return text_cleaner.clean_pdf_text(text)

    # ------------------------------------------------------------------#

    def get_total_pages(
        self,
        pdf_path: Path,
    ) -> int:
        """
        Returns total number of pages.
        """

        document = fitz.open(pdf_path)

        total_pages = document.page_count

        document.close()

        return total_pages

    # ------------------------------------------------------------------#

    def validate_pdf(
        self,
        pdf_path: Path,
    ) -> bool:
        """
        Validate PDF file.
        """

        try:

            document = fitz.open(pdf_path)

            if document.page_count == 0:
                document.close()
                return False

            document.close()

            return True

        except Exception as error:

            logger.error(error)

            return False


pdf_service = PDFService()
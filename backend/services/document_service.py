"""
File: backend/services/document_service.py

Document Management Service

Responsibilities
----------------
1. Validate uploaded files
2. Route PDFs and Images
3. Save uploaded files
4. Process uploaded documents
5. Return LangChain Documents
"""

from pathlib import Path
from typing import List

from fastapi import UploadFile
from langchain_core.documents import Document

from core.logger import logger
from utils.file_utils import file_manager

from vectorstore.chroma_manager import chroma_manager

class DocumentService:
    """
    Main service responsible for handling uploaded documents.

    It acts as the entry point for all uploaded files before
    passing them to the corresponding processing service.
    """

    def __init__(self):
        self.file_manager = file_manager
        self.vectorstore = chroma_manager

    # ---------------------------------------------------------

    async def save_pdf(
        self,
        file: UploadFile,
    ) -> Path:
        """
        Save uploaded PDF.
        """

        logger.info(f"Uploading PDF: {file.filename}")

        saved_path = await self.file_manager.save_pdf(file)

        logger.info(f"Saved PDF: {saved_path}")

        return saved_path

    # ---------------------------------------------------------

    async def save_image(
        self,
        file: UploadFile,
    ) -> Path:
        """
        Save uploaded image.
        """

        logger.info(f"Uploading Image: {file.filename}")

        saved_path = await self.file_manager.save_image(file)

        logger.info(f"Saved Image: {saved_path}")

        return saved_path

    # ---------------------------------------------------------

    async def process_pdf(
        self,
        file: UploadFile,
    ) -> List[Document]:

        from services.pdf_service import PDFService

        saved_path = await self.save_pdf(file)

        pdf_service = PDFService()

        documents = pdf_service.process_pdf(saved_path)

        if documents:

            self.vectorstore.add_documents(
                documents
            )

        logger.info(
            f"{saved_path.name} stored successfully in ChromaDB."
        )

        return documents

    # ---------------------------------------------------------

    async def process_image(
        self,
        file: UploadFile,
    ) -> List[Document]:

        from services.image_service import ImageService

        saved_path = await self.save_image(file)

        image_service = ImageService()

        documents = image_service.process_image(saved_path)

        if documents:

            self.vectorstore.add_documents(
                documents
            )

        logger.info(
            f"{saved_path.name} stored successfully in ChromaDB."
        )

        return documents

    # ---------------------------------------------------------

    def list_uploaded_pdfs(self):
        """
        Returns uploaded PDFs.
        """

        return self.file_manager.list_uploaded_pdfs()

    # ---------------------------------------------------------

    def list_uploaded_images(self):
        """
        Returns uploaded images.
        """

        return self.file_manager.list_uploaded_images()

    # ---------------------------------------------------------

    @staticmethod
    def delete_document(
        filepath: str,
    ) -> bool:
        """
        Delete uploaded document.
        """

        path = Path(filepath)

        return file_manager.delete_file(path)
    
# ---------------------------------------------------------

    def list_vector_documents(
        self,
    ):

        return self.vectorstore.list_documents()

    # ---------------------------------------------------------

    def delete_vector_document(
        self,
        filename: str,
    ):

        self.vectorstore.delete_document(
            filename
        )

    # ---------------------------------------------------------

    def vector_statistics(
        self,
    ):

        return self.vectorstore.get_collection_statistics()    


document_service = DocumentService()
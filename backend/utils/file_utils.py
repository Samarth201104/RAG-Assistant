"""
File: backend/utils/file_utils.py

Purpose
-------
Provides helper methods for file management.

Responsibilities
----------------
1. Create upload directories
2. Validate uploaded files
3. Save uploaded files
4. Delete uploaded files
5. List uploaded files
"""

from pathlib import Path
from uuid import uuid4
from typing import List

from fastapi import UploadFile

from core.config import settings
from core.constants import (
    SUPPORTED_PDF_EXTENSIONS,
    SUPPORTED_IMAGE_EXTENSIONS,
)
from core.logger import logger


class FileManager:
    """
    Handles all file-related operations.

    This class centralizes file management so the rest of the
    application doesn't need to interact with the filesystem
    directly.
    """

    def __init__(self) -> None:

        self.pdf_dir = Path(settings.UPLOAD_PDF_DIR)

        self.image_dir = Path(settings.UPLOAD_IMAGE_DIR)

        self.processed_dir = Path(settings.PROCESSED_DATA_DIR)

        self.temp_dir = Path(settings.TEMP_DIR)

        self.create_directories()

    # ---------------------------------------------------------

    def create_directories(self) -> None:
        """
        Creates all required project directories if they do not exist.
        """

        directories = [
            self.pdf_dir,
            self.image_dir,
            self.processed_dir,
            self.temp_dir,
        ]

        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)

    # ---------------------------------------------------------

    @staticmethod
    def get_extension(filename: str) -> str:
        """
        Returns file extension.

        Example
        -------
        paper.pdf -> .pdf
        """

        return Path(filename).suffix.lower()

    # ---------------------------------------------------------

    def validate_pdf(self, filename: str) -> bool:
        """
        Validate uploaded PDF.
        """

        return (
            self.get_extension(filename)
            in SUPPORTED_PDF_EXTENSIONS
        )

    # ---------------------------------------------------------

    def validate_image(self, filename: str) -> bool:
        """
        Validate uploaded image.
        """

        return (
            self.get_extension(filename)
            in SUPPORTED_IMAGE_EXTENSIONS
        )

    # ---------------------------------------------------------

    @staticmethod
    def generate_unique_filename(filename: str) -> str:
        """
        Generates a unique filename.

        Example
        -------
        paper.pdf

        becomes

        a71f23f1_paper.pdf
        """

        unique_id = uuid4().hex[:8]

        return f"{unique_id}_{filename}"

    # ---------------------------------------------------------

    async def save_pdf(
        self,
        file: UploadFile,
    ) -> Path:
        """
        Save uploaded PDF.
        """

        if not self.validate_pdf(file.filename):

            raise ValueError(
                "Unsupported PDF file."
            )

        filename = self.generate_unique_filename(
            file.filename
        )

        destination = self.pdf_dir / filename

        contents = await file.read()

        destination.write_bytes(contents)

        logger.info(f"PDF saved: {destination}")

        return destination

    # ---------------------------------------------------------

    async def save_image(
        self,
        file: UploadFile,
    ) -> Path:
        """
        Save uploaded image.
        """

        if not self.validate_image(file.filename):

            raise ValueError(
                "Unsupported image file."
            )

        filename = self.generate_unique_filename(
            file.filename
        )

        destination = self.image_dir / filename

        contents = await file.read()

        destination.write_bytes(contents)

        logger.info(f"Image saved: {destination}")

        return destination

    # ---------------------------------------------------------

    @staticmethod
    def delete_file(
        filepath: Path,
    ) -> bool:
        """
        Deletes a file.

        Returns
        -------
        True if deleted.
        """

        if filepath.exists():

            filepath.unlink()

            logger.info(f"Deleted {filepath}")

            return True

        return False

    # ---------------------------------------------------------

    def list_uploaded_pdfs(self) -> List[str]:
        """
        Returns all uploaded PDFs.
        """

        return sorted(
            [
                file.name
                for file in self.pdf_dir.glob("*.pdf")
            ]
        )

    # ---------------------------------------------------------

    def list_uploaded_images(self) -> List[str]:
        """
        Returns all uploaded images.
        """

        extensions = [
            "*.png",
            "*.jpg",
            "*.jpeg",
            "*.bmp",
            "*.tiff",
        ]

        images = []

        for extension in extensions:

            images.extend(
                self.image_dir.glob(extension)
            )

        return sorted(
            [image.name for image in images]
        )


file_manager = FileManager()
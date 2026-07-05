"""
File: backend/services/image_service.py
"""

from pathlib import Path
from typing import Dict, List

import cv2
import easyocr
from langchain_core.documents import Document

from core.logger import logger
from services.llm_service import llm_service
from utils.chunk_utils import chunk_manager
from utils.text_utils import text_cleaner


class ImageService:
    """
    Image Processing Service
    """

    def __init__(self):

        logger.info("Initializing Image Service...")

        self.reader = easyocr.Reader(
            ["en"],
            gpu=False,
        )

    # ------------------------------------------------------------------

    def process_image(
        self,
        image_path: Path,
    ) -> List[Document]:
        """
        Complete image processing pipeline.
        """

        logger.info(
            f"Processing image : {image_path.name}"
        )

        ocr_text = self.extract_text(
            image_path
        )

        image_description = (
            self.describe_image(
                image_path
            )
        )

        combined_text = self.combine_results(
            ocr_text,
            image_description,
        )

        cleaned_text = (
            text_cleaner.clean_ocr_text(
                combined_text
            )
        )

        metadata = {
            "source": image_path.name,
            "page": 1,
            "document_type": "image",
        }

        documents = (
            chunk_manager.create_chunks(
                cleaned_text,
                metadata,
            )
        )

        logger.info(
            f"{image_path.name} processed successfully."
        )

        return documents

    # ------------------------------------------------------------------

    def extract_text(
        self,
        image_path: Path,
    ) -> str:
        """
        OCR using EasyOCR.
        """

        image = cv2.imread(
            str(image_path)
        )

        if image is None:

            raise ValueError(
                f"Unable to open image : {image_path}"
            )

        results = self.reader.readtext(
            image
        )

        extracted_text = "\n".join(
            result[1]
            for result in results
        )

        logger.info(
            f"OCR completed : {image_path.name}"
        )

        return extracted_text

    # ------------------------------------------------------------------

    def describe_image(
        self,
        image_path: Path,
    ) -> str:
        """
        Generate semantic image description
        using Gemini Vision.
        """

        prompt = """
You are an AI Research Assistant.

Analyze this image carefully.

Describe:

1. Overall scene

2. Diagrams

3. Flowcharts

4. Graphs

5. Tables

6. Important labels

7. Mathematical equations

8. Technical content

9. Relationships between objects

10. Everything useful for semantic retrieval.

Return a detailed description.
"""

        response = llm_service.invoke_multimodal(
            image_path=image_path,
            prompt=prompt,
        )

        logger.info(
            f"Gemini Vision completed : {image_path.name}"
        )

        return response

    # ------------------------------------------------------------------

    @staticmethod
    def combine_results(
        ocr_text: str,
        image_description: str,
    ) -> str:
        """
        Combine OCR and Vision output.
        """

        return f"""
================ OCR =================

{ocr_text}

======================================

================ VISION ==============

{image_description}

======================================
"""

    # ------------------------------------------------------------------

    @staticmethod
    def validate_image(
        image_path: Path,
    ) -> bool:
        """
        Validate image.
        """

        image = cv2.imread(
            str(image_path)
        )

        return image is not None

    # ------------------------------------------------------------------

    @staticmethod
    def get_image_information(
        image_path: Path,
    ) -> Dict:
        """
        Return image metadata.
        """

        image = cv2.imread(
            str(image_path)
        )

        if image is None:

            raise ValueError(
                f"Unable to open image : {image_path}"
            )

        height, width, channels = image.shape

        return {
            "filename": image_path.name,
            "width": width,
            "height": height,
            "channels": channels,
            "size_mb": round(
                image_path.stat().st_size
                / (1024 * 1024),
                2,
            ),
        }


image_service = ImageService()
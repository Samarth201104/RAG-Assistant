"""
File: backend/utils/text_utils.py

Purpose
-------
Provides reusable text preprocessing utilities for the
MultiModal RAG Research Assistant.

Responsibilities
----------------
1. Clean extracted PDF text
2. Clean OCR text
3. Normalize whitespace
4. Remove unwanted characters
5. Validate extracted text
"""

import re
from typing import List


class TextCleaner:
    """
    Utility class for cleaning text before chunking
    and embedding.
    """

    @staticmethod
    def normalize_whitespace(text: str) -> str:
        """
        Replace multiple spaces/tabs with a single space.
        """

        text = re.sub(r"[ \t]+", " ", text)

        return text.strip()

    # --------------------------------------------------

    @staticmethod
    def normalize_newlines(text: str) -> str:
        """
        Replace multiple blank lines with a single blank line.
        """

        text = re.sub(r"\n{2,}", "\n\n", text)

        return text.strip()

    # --------------------------------------------------

    @staticmethod
    def remove_unicode_artifacts(text: str) -> str:
        """
        Remove unwanted unicode characters that commonly
        appear after PDF extraction.
        """

        replacements = {
            "\u00a0": " ",     # Non-breaking space
            "\uf0b7": "-",     # Bullet
            "\ufeff": "",      # BOM
            "\xad": "",        # Soft hyphen
        }

        for old, new in replacements.items():
            text = text.replace(old, new)

        return text

    # --------------------------------------------------

    @staticmethod
    def remove_extra_punctuation(text: str) -> str:
        """
        Compress repeated punctuation.

        Example:
        --------
        Hello..... -> Hello.
        """

        text = re.sub(r"\.{2,}", ".", text)
        text = re.sub(r"-{3,}", "--", text)

        return text

    # --------------------------------------------------

    @staticmethod
    def clean_pdf_text(text: str) -> str:
        """
        Cleaning pipeline for PDF extracted text.
        """

        text = TextCleaner.remove_unicode_artifacts(text)

        text = TextCleaner.normalize_whitespace(text)

        text = TextCleaner.normalize_newlines(text)

        text = TextCleaner.remove_extra_punctuation(text)

        return text.strip()

    # --------------------------------------------------

    @staticmethod
    def clean_ocr_text(text: str) -> str:
        """
        OCR output usually contains additional spaces
        and line breaks.
        """

        text = TextCleaner.normalize_whitespace(text)

        text = TextCleaner.normalize_newlines(text)

        return text.strip()

    # --------------------------------------------------

    @staticmethod
    def remove_empty_lines(text: str) -> str:
        """
        Remove empty lines.
        """

        lines = text.splitlines()

        cleaned_lines = [
            line.strip()
            for line in lines
            if line.strip()
        ]

        return "\n".join(cleaned_lines)

    # --------------------------------------------------

    @staticmethod
    def validate_text(text: str) -> bool:
        """
        Check if extracted text contains useful content.
        """

        return bool(text and text.strip())

    # --------------------------------------------------

    @staticmethod
    def split_into_paragraphs(text: str) -> List[str]:
        """
        Split text into paragraphs.
        """

        paragraphs = [
            paragraph.strip()
            for paragraph in text.split("\n\n")
            if paragraph.strip()
        ]

        return paragraphs


text_cleaner = TextCleaner()
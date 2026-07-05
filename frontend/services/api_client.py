"""
File: frontend/services/api_client.py

HTTP Client for FastAPI Backend
"""

from __future__ import annotations

from typing import Any

import requests

from utils.constants import (
    API_TIMEOUT,
    BACKEND_URL,
    HEALTH_ENDPOINT,
    UPLOAD_PDF_ENDPOINT,
    UPLOAD_IMAGE_ENDPOINT,
    LIST_DOCUMENTS_ENDPOINT,
    DELETE_DOCUMENT_ENDPOINT,
    VECTOR_STATISTICS_ENDPOINT,
    QUERY_ENDPOINT,
    SUMMARY_ENDPOINT,
    COMPARE_ENDPOINT,
    NOTES_ENDPOINT,
)

# =============================================================================
# API Client
# =============================================================================

class APIClient:
    """
    Centralized HTTP client for communicating with
    the FastAPI backend.
    """

    def __init__(
        self,
        base_url: str = BACKEND_URL,
        timeout: int = API_TIMEOUT,
    ) -> None:

        self.base_url = base_url.rstrip("/")

        self.timeout = timeout

        self.session = requests.Session()

    # =========================================================================
    # Internal Request Handler
    # =========================================================================

    def _request(
        self,
        method: str,
        endpoint: str,
        **kwargs,
    ) -> dict:
        """
        Execute an HTTP request.

        Returns
        -------
        dict
            Standardized response.
        """

        url = f"{self.base_url}{endpoint}"

        try:

            response = self.session.request(

                method=method,

                url=url,

                timeout=self.timeout,

                **kwargs,

            )

            response.raise_for_status()

            if response.content:

                data = response.json()

            else:

                data = {}

            return {

                "success": True,

                "status_code": response.status_code,

                "data": data,

                "message": data.get(
                    "message",
                    "Success",
                ),

            }

        except requests.exceptions.HTTPError as error:

            try:

                message = error.response.json().get(
                    "detail",
                    str(error),
                )

            except Exception:

                message = str(error)

            return {

                "success": False,

                "status_code": getattr(
                    error.response,
                    "status_code",
                    500,
                ),

                "data": {},

                "message": message,

            }

        except requests.exceptions.ConnectionError:

            return {

                "success": False,

                "status_code": 503,

                "data": {},

                "message": "Unable to connect to backend server.",

            }

        except requests.exceptions.Timeout:

            return {

                "success": False,

                "status_code": 408,

                "data": {},

                "message": "Request timed out.",

            }

        except Exception as error:

            return {

                "success": False,

                "status_code": 500,

                "data": {},

                "message": str(error),

            }

    # =========================================================================
    # Health
    # =========================================================================

    def health(
        self,
    ) -> dict:
        """
        Backend health.
        """

        return self._request(

            "GET",

            HEALTH_ENDPOINT,

        )

    # =========================================================================
    # Upload PDF
    # =========================================================================

    def upload_pdf(
        self,
        files: list,
    ) -> dict:
        """
        Upload PDF documents.
        """

        payload = [

            (

                "files",

                (

                    file.name,

                    file,

                    "application/pdf",

                ),

            )

            for file in files

        ]

        return self._request(

            "POST",

            UPLOAD_PDF_ENDPOINT,

            files=payload,

        )

    # =========================================================================
    # Upload Images
    # =========================================================================

    def upload_images(
        self,
        files: list,
    ) -> dict:
        """
        Upload image files.
        """

        payload = [

            (

                "files",

                (

                    file.name,

                    file,

                    file.type,

                ),

            )

            for file in files

        ]

        return self._request(

            "POST",

            UPLOAD_IMAGE_ENDPOINT,

            files=payload,

        )

    # =========================================================================
    # List Documents
    # =========================================================================

    def list_documents(
        self,
    ) -> list:
        """
        Return indexed documents.
        """

        response = self._request(

            "GET",

            LIST_DOCUMENTS_ENDPOINT,

        )

        if response["success"]:

            return response["data"]

        return []

    # =========================================================================
    # Vector Statistics
    # =========================================================================

    def vector_statistics(
        self,
    ) -> dict:
        """
        Return vector database statistics.
        """

        response = self._request(

            "GET",

            VECTOR_STATISTICS_ENDPOINT,

        )

        if response["success"]:

            return response["data"]

        return {}
    
    # =========================================================================
    # Delete Document
    # =========================================================================

    def delete_document(
        self,
        filename: str,
    ) -> dict:
        """
        Delete an indexed document.
        """

        return self._request(

            "DELETE",

            f"{DELETE_DOCUMENT_ENDPOINT}/{filename}",

        )

    # =========================================================================
    # Chat Query
    # =========================================================================

    def query(
        self,
        question: str,
        top_k: int = 5,
    ) -> dict:
        """
        Query the RAG system.
        """

        payload = {

            "question": question,

            "top_k": top_k,

        }

        return self._request(

            "POST",

            QUERY_ENDPOINT,

            json=payload,

        )

    # =========================================================================
    # Summarize
    # =========================================================================

    def summarize(
        self,
        filename: str,
    ) -> dict:
        """
        Generate document summary.
        """

        payload = {

            "filename": filename,

        }

        return self._request(

            "POST",

            SUMMARY_ENDPOINT,

            json=payload,

        )

    # =========================================================================
    # Compare Documents
    # =========================================================================

    def compare(
        self,
        document_one: str,
        document_two: str,
    ) -> dict:
        """
        Compare two indexed documents.
        """

        payload = {

            "document_one": document_one,

            "document_two": document_two,

        }

        return self._request(

            "POST",

            COMPARE_ENDPOINT,

            json=payload,

        )

    # =========================================================================
    # Generate Notes
    # =========================================================================

    def generate_notes(
        self,
        filename: str,
    ) -> dict:
        """
        Generate study notes.
        """

        payload = {

            "filename": filename,

        }

        return self._request(

            "POST",

            NOTES_ENDPOINT,

            json=payload,

        )

    # =========================================================================
    # Backend Information
    # =========================================================================

    def backend_available(
        self,
    ) -> bool:
        """
        Check backend availability.
        """

        return self.health().get(
            "success",
            False,
        )

    # =========================================================================
    # Close Session
    # =========================================================================

    def close(
        self,
    ) -> None:
        """
        Close HTTP session.
        """

        self.session.close()


# =============================================================================
# Singleton Instance
# =============================================================================

api_client = APIClient()
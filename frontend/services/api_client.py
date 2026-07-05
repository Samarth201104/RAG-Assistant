"""
File: frontend/services/api_client.py

Enterprise HTTP Client
MultiModal RAG Research Assistant
"""

from __future__ import annotations

from typing import Any

import requests

from utils.constants import (
    API_TIMEOUT,
    BACKEND_URL,
    HEALTH_ENDPOINT,
)


# =============================================================================
# API Client
# =============================================================================

class APIClient:
    """
    Enterprise HTTP client for communicating with
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

        {
            success: bool,
            message: str,
            data: Any,
            status_code: int
        }
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

            payload = {}

            if response.content:

                payload = response.json()

            # --------------------------------------------------------------
            # Normalize backend responses
            #
            # Upload APIs
            # {
            #     success,
            #     message,
            #     data
            # }
            #
            # AI APIs
            # {
            #     success,
            #     message,
            #     response
            # }
            # --------------------------------------------------------------

            normalized_data = payload.get(
                "data",
                payload.get(
                    "response",
                    payload,
                ),
            )

            return {

                "success": payload.get(
                    "success",
                    True,
                ),

                "message": payload.get(
                    "message",
                    "Success",
                ),

                "data": normalized_data,

                "status_code": response.status_code,

            }

        except requests.exceptions.Timeout:

            return {

                "success": False,

                "message": "Request timed out.",

                "data": {},

                "status_code": 408,

            }

        except requests.exceptions.ConnectionError:

            return {

                "success": False,

                "message": "Unable to connect to backend server.",

                "data": {},

                "status_code": 503,

            }

        except requests.exceptions.HTTPError as error:

            try:

                detail = error.response.json().get(
                    "detail",
                    str(error),
                )

            except Exception:

                detail = str(error)

            return {

                "success": False,

                "message": detail,

                "data": {},

                "status_code": getattr(
                    error.response,
                    "status_code",
                    500,
                ),

            }

        except Exception as error:

            return {

                "success": False,

                "message": str(error),

                "data": {},

                "status_code": 500,

            }

    # =========================================================================
    # Health APIs
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

    def ready(
        self,
    ) -> dict:
        """
        Readiness probe.
        """

        return self._request(

            "GET",

            f"{HEALTH_ENDPOINT}/ready",

        )

    def live(
        self,
    ) -> dict:
        """
        Liveness probe.
        """

        return self._request(

            "GET",

            f"{HEALTH_ENDPOINT}/live",

        )

    def configuration(
        self,
    ) -> dict:
        """
        Backend configuration.
        """

        return self._request(

            "GET",

            f"{HEALTH_ENDPOINT}/config",

        )

    def vectordb_health(
        self,
    ) -> dict:
        """
        ChromaDB statistics.
        """

        return self._request(

            "GET",

            f"{HEALTH_ENDPOINT}/vectordb",

        )

    def backend_available(
        self,
    ) -> bool:
        """
        Backend availability.
        """

        response = self.health()

        return response.get(
            "success",
            False,
        )
    
    # =========================================================================
    # Upload APIs
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

            "/upload/pdf",

            files=payload,

        )

    def upload_images(
        self,
        files: list,
    ) -> dict:
        """
        Upload image documents.
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

            "/upload/image",

            files=payload,

        )

    # =========================================================================
    # Document APIs
    # =========================================================================

    def list_documents(
        self,
    ) -> list:
        """
        List indexed ChromaDB documents.
        """

        response = self._request(

            "GET",

            "/upload/documents",

        )

        if response["success"]:

            return response["data"].get(

                "documents",

                [],

            )

        return []

    def list_uploaded_pdfs(
        self,
    ) -> list:
        """
        List uploaded PDFs.
        """

        response = self._request(

            "GET",

            "/upload/pdfs",

        )

        if response["success"]:

            return response["data"].get(

                "documents",

                [],

            )

        return []

    def list_uploaded_images(
        self,
    ) -> list:
        """
        List uploaded images.
        """

        response = self._request(

            "GET",

            "/upload/images",

        )

        if response["success"]:

            return response["data"].get(

                "images",

                [],

            )

        return []

    # =========================================================================
    # Delete Document
    # =========================================================================

    def delete_document(
        self,
        filename: str,
    ) -> dict:
        """
        Delete document from ChromaDB.
        """

        return self._request(

            "DELETE",

            f"/upload/document/{filename}",

        )

    # =========================================================================
    # Vector Database
    # =========================================================================

    def vector_statistics(
        self,
    ) -> dict:
        """
        Return vector database statistics.
        """

        response = self._request(

            "GET",

            "/upload/statistics",

        )

        if response["success"]:

            return response["data"]

        return {}

    # =========================================================================
    # Collection Information
    # =========================================================================

    def collection_summary(
        self,
    ) -> dict:
        """
        Return a summary of the current collection.
        """

        documents = self.list_documents()

        statistics = self.vector_statistics()

        return {

            "documents": documents,

            "document_count": len(documents),

            "statistics": statistics,

        }
    
    # =========================================================================
    # Internal AI Helpers
    # =========================================================================

    def _post_json(
        self,
        endpoint: str,
        payload: dict,
    ) -> dict:
        """
        Send JSON POST request.
        """

        return self._request(

            "POST",

            endpoint,

            json=payload,

        )

    def _summary_request(
        self,
        endpoint: str,
        filename: str,
    ) -> dict:
        """
        Execute summarization request.
        """

        return self._post_json(

            endpoint,

            {

                "filename": filename,

            },

        )

    # =========================================================================
    # Query APIs
    # =========================================================================

    def query(
        self,
        question: str,
        top_k: int = 5,
    ) -> dict:
        """
        Query all indexed documents.
        """

        return self._post_json(

            "/query",

            {

                "question": question,

                "top_k": top_k,

            },

        )

    def query_document(
        self,
        filename: str,
        question: str,
        top_k: int = 5,
    ) -> dict:
        """
        Query a single document.
        """

        return self._post_json(

            "/query/document",

            {

                "filename": filename,

                "question": question,

                "top_k": top_k,

            },

        )

    def retrieve_chunks(
        self,
        question: str,
        top_k: int = 5,
    ) -> dict:
        """
        Retrieve relevant chunks only.
        """

        return self._post_json(

            "/query/retrieve",

            {

                "question": question,

                "top_k": top_k,

            },

        )

    # =========================================================================
    # Summarization APIs
    # =========================================================================

    def summarize(
        self,
        filename: str,
    ) -> dict:

        return self._summary_request(

            "/summarize",

            filename,

        )

    def executive_summary(
        self,
        filename: str,
    ) -> dict:

        return self._summary_request(

            "/summarize/executive",

            filename,

        )

    def key_findings(
        self,
        filename: str,
    ) -> dict:

        return self._summary_request(

            "/summarize/key-findings",

            filename,

        )

    def methodology_summary(
        self,
        filename: str,
    ) -> dict:

        return self._summary_request(

            "/summarize/methodology",

            filename,

        )

    def limitations_summary(
        self,
        filename: str,
    ) -> dict:

        return self._summary_request(

            "/summarize/limitations",

            filename,

        )

    def future_work_summary(
        self,
        filename: str,
    ) -> dict:

        return self._summary_request(

            "/summarize/future-work",

            filename,

        )

    def contribution_summary(
        self,
        filename: str,
    ) -> dict:

        return self._summary_request(

            "/summarize/contribution",

            filename,

        )

    def abstract_summary(
        self,
        filename: str,
    ) -> dict:

        return self._summary_request(

            "/summarize/abstract",

            filename,

        )

    def one_line_summary(
        self,
        filename: str,
    ) -> dict:

        return self._summary_request(

            "/summarize/one-line",

            filename,

        )

    def tldr_summary(
        self,
        filename: str,
    ) -> dict:

        return self._summary_request(

            "/summarize/tldr",

            filename,

        )

    def complete_summary(
        self,
        filename: str,
    ) -> dict:

        return self._summary_request(

            "/summarize/all",

            filename,

        )
    
    # =========================================================================
    # Internal Comparison Helper
    # =========================================================================

    def _compare_request(
        self,
        endpoint: str,
        document_1: str,
        document_2: str,
    ) -> dict:
        """
        Execute comparison request.
        """

        return self._post_json(

            endpoint,

            {

                "document_1": document_1,

                "document_2": document_2,

            },

        )

    # =========================================================================
    # Comparison APIs
    # =========================================================================

    def compare(
        self,
        document_1: str,
        document_2: str,
    ) -> dict:

        return self._compare_request(
            "/compare",
            document_1,
            document_2,
        )

    def similarities(
        self,
        document_1: str,
        document_2: str,
    ) -> dict:

        return self._compare_request(
            "/compare/similarities",
            document_1,
            document_2,
        )

    def differences(
        self,
        document_1: str,
        document_2: str,
    ) -> dict:

        return self._compare_request(
            "/compare/differences",
            document_1,
            document_2,
        )

    def methodology_comparison(
        self,
        document_1: str,
        document_2: str,
    ) -> dict:

        return self._compare_request(
            "/compare/methodology",
            document_1,
            document_2,
        )

    def results_comparison(
        self,
        document_1: str,
        document_2: str,
    ) -> dict:

        return self._compare_request(
            "/compare/results",
            document_1,
            document_2,
        )

    def advantages_limitations(
        self,
        document_1: str,
        document_2: str,
    ) -> dict:

        return self._compare_request(
            "/compare/advantages-limitations",
            document_1,
            document_2,
        )

    def best_paper(
        self,
        document_1: str,
        document_2: str,
    ) -> dict:

        return self._compare_request(
            "/compare/best-paper",
            document_1,
            document_2,
        )

    def technical_comparison(
        self,
        document_1: str,
        document_2: str,
    ) -> dict:

        return self._compare_request(
            "/compare/technical",
            document_1,
            document_2,
        )

    def comparison_table(
        self,
        document_1: str,
        document_2: str,
    ) -> dict:

        return self._compare_request(
            "/compare/table",
            document_1,
            document_2,
        )

    def complete_comparison(
        self,
        document_1: str,
        document_2: str,
    ) -> dict:

        return self._compare_request(
            "/compare/all",
            document_1,
            document_2,
        )

    # =========================================================================
    # Internal Notes Helper
    # =========================================================================

    def _notes_request(
        self,
        endpoint: str,
        filename: str,
        note_type: str | None = None,
    ) -> dict:
        """
        Execute notes request.
        """

        payload = {

            "filename": filename,

        }

        if note_type is not None:

            payload["note_type"] = note_type

        return self._post_json(
            endpoint,
            payload,
        )

    # =========================================================================
    # Notes APIs
    # =========================================================================

    def generate_notes(
        self,
        filename: str,
        note_type: str,
    ) -> dict:

        return self._notes_request(
            "/notes",
            filename,
            note_type,
        )

    def short_notes(self, filename: str) -> dict:
        return self._notes_request("/notes/short", filename)

    def detailed_notes(self, filename: str) -> dict:
        return self._notes_request("/notes/detailed", filename)

    def flashcards(self, filename: str) -> dict:
        return self._notes_request("/notes/flashcards", filename)

    def interview_questions(self, filename: str) -> dict:
        return self._notes_request("/notes/interview", filename)

    def viva_questions(self, filename: str) -> dict:
        return self._notes_request("/notes/viva", filename)

    def mcqs(self, filename: str) -> dict:
        return self._notes_request("/notes/mcq", filename)

    def revision_notes(self, filename: str) -> dict:
        return self._notes_request("/notes/revision", filename)

    def cheat_sheet(self, filename: str) -> dict:
        return self._notes_request("/notes/cheatsheet", filename)

    def mind_map(self, filename: str) -> dict:
        return self._notes_request("/notes/mindmap", filename)

    def faqs(self, filename: str) -> dict:
        return self._notes_request("/notes/faq", filename)

    def exam_preparation(self, filename: str) -> dict:
        return self._notes_request("/notes/exam", filename)

    def concept_explanation(self, filename: str) -> dict:
        return self._notes_request("/notes/concept", filename)

    def complete_notes(self, filename: str) -> dict:
        return self._notes_request("/notes/all", filename)

    # =========================================================================
    # Session
    # =========================================================================

    def close(
        self,
    ) -> None:
        """
        Close HTTP session.
        """

        self.session.close()


# =============================================================================
# Singleton
# =============================================================================

api_client = APIClient()
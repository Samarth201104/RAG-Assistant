"""
File: backend/services/summarization_service.py
"""

from typing import Dict

from core.logger import logger

from prompts.summarize_prompts import (
    ABSTRACT_PROMPT,
    CONTRIBUTION_PROMPT,
    EXECUTIVE_SUMMARY_PROMPT,
    FUTURE_WORK_PROMPT,
    KEY_FINDINGS_PROMPT,
    LIMITATIONS_PROMPT,
    METHODOLOGY_PROMPT,
    ONE_LINE_SUMMARY_PROMPT,
    SUMMARY_PROMPT,
    TLDR_PROMPT,
)

from services.llm_service import llm_service
from services.retrieval_service import retrieval_service


class SummarizationService:
    """
    Research Paper Summarization Service.
    Uses the complete document instead of Top-K retrieval.
    """

    def __init__(self):

        self.llm = llm_service
        self.retriever = retrieval_service

    # ------------------------------------------------------------------

    def _generate(
        self,
        filename: str,
        prompt_template: str,
        system_prompt: str = "You are an AI Research Assistant.",
    ) -> str:
        """
        Generic summary generator.
        """

        logger.info(
            f"Generating content for document: {filename}"
        )

        context = self.retriever.get_document_context(
            filename
        )

        if not context.strip():

            raise ValueError(
                f"No content found for '{filename}'."
            )

        prompt = prompt_template.format(
            context=context
        )

        return self.llm.invoke(
            system_prompt=system_prompt,
            user_prompt=prompt,
        )

    # ------------------------------------------------------------------

    def summarize(
        self,
        filename: str,
    ) -> Dict:

        summary = self._generate(
            filename,
            SUMMARY_PROMPT,
        )

        return {
            "filename": filename,
            "summary": summary,
        }

    # ------------------------------------------------------------------

    def executive_summary(
        self,
        filename: str,
    ) -> str:

        return self._generate(
            filename,
            EXECUTIVE_SUMMARY_PROMPT,
        )

    # ------------------------------------------------------------------

    def key_findings(
        self,
        filename: str,
    ) -> str:

        return self._generate(
            filename,
            KEY_FINDINGS_PROMPT,
        )

    # ------------------------------------------------------------------

    def methodology(
        self,
        filename: str,
    ) -> str:

        return self._generate(
            filename,
            METHODOLOGY_PROMPT,
        )

    # ------------------------------------------------------------------

    def limitations(
        self,
        filename: str,
    ) -> str:

        return self._generate(
            filename,
            LIMITATIONS_PROMPT,
        )

    # ------------------------------------------------------------------

    def future_work(
        self,
        filename: str,
    ) -> str:

        return self._generate(
            filename,
            FUTURE_WORK_PROMPT,
        )

    # ------------------------------------------------------------------

    def contribution(
        self,
        filename: str,
    ) -> str:

        return self._generate(
            filename,
            CONTRIBUTION_PROMPT,
        )

    # ------------------------------------------------------------------

    def abstract(
        self,
        filename: str,
    ) -> str:

        return self._generate(
            filename,
            ABSTRACT_PROMPT,
        )

    # ------------------------------------------------------------------

    def one_line_summary(
        self,
        filename: str,
    ) -> str:

        return self._generate(
            filename,
            ONE_LINE_SUMMARY_PROMPT,
        )

    # ------------------------------------------------------------------

    def tldr(
        self,
        filename: str,
    ) -> str:

        return self._generate(
            filename,
            TLDR_PROMPT,
        )

    # ------------------------------------------------------------------

    def generate_all(
        self,
        filename: str,
    ) -> Dict:
        """
        Generate all available summaries in one API call.
        """

        logger.info(
            f"Generating complete summary package for: {filename}"
        )

        return {
            "filename": filename,
            "executive_summary": self.executive_summary(filename),
            "key_findings": self.key_findings(filename),
            "methodology": self.methodology(filename),
            "limitations": self.limitations(filename),
            "future_work": self.future_work(filename),
            "contribution": self.contribution(filename),
            "abstract": self.abstract(filename),
            "one_line_summary": self.one_line_summary(filename),
            "tldr": self.tldr(filename),
        }

    # ------------------------------------------------------------------

    def health_check(self):

        return {
            "service": "Summarization Service",
            "model": self.llm.get_model_name(),
            "status": "Running",
        }


summarization_service = SummarizationService()
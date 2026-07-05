"""
File: backend/services/compare_service.py
"""

from typing import Dict

from core.logger import logger

from prompts.compare_prompts import (
    ADVANTAGES_LIMITATIONS_PROMPT,
    BEST_PAPER_PROMPT,
    COMPARE_PROMPT,
    COMPARISON_TABLE_PROMPT,
    DIFFERENCES_PROMPT,
    METHODOLOGY_COMPARISON_PROMPT,
    RESULT_COMPARISON_PROMPT,
    SIMILARITIES_PROMPT,
    TECHNICAL_COMPARISON_PROMPT,
)

from services.llm_service import llm_service
from services.retrieval_service import retrieval_service


class CompareService:
    """
    Research Paper Comparison Service.
    """

    def __init__(self):

        self.llm = llm_service
        self.retriever = retrieval_service

    # ------------------------------------------------------------------

    def _generate(
        self,
        document_1: str,
        document_2: str,
        prompt_template: str,
        system_prompt: str = "You are a Senior AI Research Engineer.",
    ) -> str:
        """
        Generic comparison generator.
        """

        logger.info(
            f"Comparing '{document_1}' with '{document_2}'"
        )

        context_1 = self.retriever.get_document_context(
            document_1
        )

        context_2 = self.retriever.get_document_context(
            document_2
        )

        if not context_1.strip():

            raise ValueError(
                f"No content found for '{document_1}'."
            )

        if not context_2.strip():

            raise ValueError(
                f"No content found for '{document_2}'."
            )

        prompt = prompt_template.format(
            paper_1=context_1,
            paper_2=context_2,
        )

        return self.llm.invoke(
            system_prompt=system_prompt,
            user_prompt=prompt,
        )

    # ------------------------------------------------------------------

    def compare(
        self,
        document_1: str,
        document_2: str,
    ) -> Dict:

        comparison = self._generate(
            document_1,
            document_2,
            COMPARE_PROMPT,
        )

        return {
            "document_1": document_1,
            "document_2": document_2,
            "comparison": comparison,
        }

    # ------------------------------------------------------------------

    def similarities(
        self,
        document_1: str,
        document_2: str,
    ) -> str:

        return self._generate(
            document_1,
            document_2,
            SIMILARITIES_PROMPT,
        )

    # ------------------------------------------------------------------

    def differences(
        self,
        document_1: str,
        document_2: str,
    ) -> str:

        return self._generate(
            document_1,
            document_2,
            DIFFERENCES_PROMPT,
        )

    # ------------------------------------------------------------------

    def methodology(
        self,
        document_1: str,
        document_2: str,
    ) -> str:

        return self._generate(
            document_1,
            document_2,
            METHODOLOGY_COMPARISON_PROMPT,
        )

    # ------------------------------------------------------------------

    def results(
        self,
        document_1: str,
        document_2: str,
    ) -> str:

        return self._generate(
            document_1,
            document_2,
            RESULT_COMPARISON_PROMPT,
        )

    # ------------------------------------------------------------------

    def advantages_limitations(
        self,
        document_1: str,
        document_2: str,
    ) -> str:

        return self._generate(
            document_1,
            document_2,
            ADVANTAGES_LIMITATIONS_PROMPT,
        )

    # ------------------------------------------------------------------

    def best_paper(
        self,
        document_1: str,
        document_2: str,
    ) -> str:

        return self._generate(
            document_1,
            document_2,
            BEST_PAPER_PROMPT,
        )

    # ------------------------------------------------------------------

    def technical_comparison(
        self,
        document_1: str,
        document_2: str,
    ) -> str:

        return self._generate(
            document_1,
            document_2,
            TECHNICAL_COMPARISON_PROMPT,
        )

    # ------------------------------------------------------------------

    def comparison_table(
        self,
        document_1: str,
        document_2: str,
    ) -> str:

        return self._generate(
            document_1,
            document_2,
            COMPARISON_TABLE_PROMPT,
        )

    # ------------------------------------------------------------------

    def generate_all(
        self,
        document_1: str,
        document_2: str,
    ) -> Dict:
        """
        Generate complete comparison package.
        """

        logger.info(
            f"Generating complete comparison package for "
            f"'{document_1}' and '{document_2}'."
        )

        return {
            "document_1": document_1,
            "document_2": document_2,
            "executive_comparison": self.compare(
                document_1,
                document_2,
            )["comparison"],
            "similarities": self.similarities(
                document_1,
                document_2,
            ),
            "differences": self.differences(
                document_1,
                document_2,
            ),
            "methodology": self.methodology(
                document_1,
                document_2,
            ),
            "results": self.results(
                document_1,
                document_2,
            ),
            "advantages_limitations": self.advantages_limitations(
                document_1,
                document_2,
            ),
            "best_paper": self.best_paper(
                document_1,
                document_2,
            ),
            "technical_comparison": self.technical_comparison(
                document_1,
                document_2,
            ),
            "comparison_table": self.comparison_table(
                document_1,
                document_2,
            ),
        }

    # ------------------------------------------------------------------

    def health_check(self):

        return {
            "service": "Compare Service",
            "model": self.llm.get_model_name(),
            "status": "Running",
        }


compare_service = CompareService()
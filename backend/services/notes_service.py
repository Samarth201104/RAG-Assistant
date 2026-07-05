"""
File: backend/services/notes_service.py
"""

from typing import Dict

from core.logger import logger

from prompts.notes_prompts import (
    CHEAT_SHEET_PROMPT,
    CONCEPT_EXPLANATION_PROMPT,
    DETAILED_NOTES_PROMPT,
    EXAM_PREPARATION_PROMPT,
    FAQ_PROMPT,
    FLASHCARD_PROMPT,
    INTERVIEW_QUESTIONS_PROMPT,
    MCQ_PROMPT,
    MINDMAP_PROMPT,
    NOTES_PROMPT,
    REVISION_PROMPT,
    SHORT_NOTES_PROMPT,
    VIVA_PROMPT,
)

from services.llm_service import llm_service
from services.retrieval_service import retrieval_service


class NotesService:
    """
    Study Notes Generation Service.
    """

    def __init__(self):

        self.llm = llm_service
        self.retriever = retrieval_service

    # ------------------------------------------------------------------

    def _generate(
        self,
        filename: str,
        prompt_template: str,
        system_prompt: str = "You are an AI Tutor and Research Assistant.",
    ) -> str:
        """
        Generic notes generator.
        """

        logger.info(
            f"Generating notes for document: {filename}"
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

    def generate_notes(
        self,
        filename: str,
    ) -> Dict:

        notes = self._generate(
            filename,
            NOTES_PROMPT,
        )

        return {
            "filename": filename,
            "notes": notes,
        }

    # ------------------------------------------------------------------

    def short_notes(
        self,
        filename: str,
    ) -> str:

        return self._generate(
            filename,
            SHORT_NOTES_PROMPT,
        )

    # ------------------------------------------------------------------

    def detailed_notes(
        self,
        filename: str,
    ) -> str:

        return self._generate(
            filename,
            DETAILED_NOTES_PROMPT,
        )

    # ------------------------------------------------------------------

    def flashcards(
        self,
        filename: str,
    ) -> str:

        return self._generate(
            filename,
            FLASHCARD_PROMPT,
        )

    # ------------------------------------------------------------------

    def interview_questions(
        self,
        filename: str,
    ) -> str:

        return self._generate(
            filename,
            INTERVIEW_QUESTIONS_PROMPT,
        )

    # ------------------------------------------------------------------

    def viva_questions(
        self,
        filename: str,
    ) -> str:

        return self._generate(
            filename,
            VIVA_PROMPT,
        )

    # ------------------------------------------------------------------

    def mcqs(
        self,
        filename: str,
    ) -> str:

        return self._generate(
            filename,
            MCQ_PROMPT,
        )

    # ------------------------------------------------------------------

    def revision_notes(
        self,
        filename: str,
    ) -> str:

        return self._generate(
            filename,
            REVISION_PROMPT,
        )

    # ------------------------------------------------------------------

    def cheat_sheet(
        self,
        filename: str,
    ) -> str:

        return self._generate(
            filename,
            CHEAT_SHEET_PROMPT,
        )

    # ------------------------------------------------------------------

    def mind_map(
        self,
        filename: str,
    ) -> str:

        return self._generate(
            filename,
            MINDMAP_PROMPT,
        )

    # ------------------------------------------------------------------

    def faqs(
        self,
        filename: str,
    ) -> str:

        return self._generate(
            filename,
            FAQ_PROMPT,
        )

    # ------------------------------------------------------------------

    def exam_preparation(
        self,
        filename: str,
    ) -> str:

        return self._generate(
            filename,
            EXAM_PREPARATION_PROMPT,
        )

    # ------------------------------------------------------------------

    def concept_explanation(
        self,
        filename: str,
    ) -> str:

        return self._generate(
            filename,
            CONCEPT_EXPLANATION_PROMPT,
        )

    # ------------------------------------------------------------------

    def generate_by_type(
        self,
        filename: str,
        note_type: str,
    ) -> Dict:
        """
        Generate notes based on note type.
        """

        note_type = note_type.lower()

        mapping = {

            "short": self.short_notes,

            "detailed": self.detailed_notes,

            "flashcards": self.flashcards,

            "interview": self.interview_questions,

            "viva": self.viva_questions,

            "mcq": self.mcqs,

            "revision": self.revision_notes,

            "cheatsheet": self.cheat_sheet,

            "mindmap": self.mind_map,

            "faq": self.faqs,

            "exam": self.exam_preparation,

            "concept": self.concept_explanation,

        }

        if note_type not in mapping:

            raise ValueError(
                f"Unsupported note type: {note_type}"
            )

        return {
            "filename": filename,
            "note_type": note_type,
            "content": mapping[note_type](filename),
        }

    # ------------------------------------------------------------------

    def generate_all(
        self,
        filename: str,
    ) -> Dict:
        """
        Generate every note type.
        """

        logger.info(
            f"Generating complete study package for {filename}"
        )

        return {

            "filename": filename,

            "short_notes":
                self.short_notes(filename),

            "detailed_notes":
                self.detailed_notes(filename),

            "flashcards":
                self.flashcards(filename),

            "interview_questions":
                self.interview_questions(filename),

            "viva_questions":
                self.viva_questions(filename),

            "mcqs":
                self.mcqs(filename),

            "revision_notes":
                self.revision_notes(filename),

            "cheat_sheet":
                self.cheat_sheet(filename),

            "mind_map":
                self.mind_map(filename),

            "faqs":
                self.faqs(filename),

            "exam_preparation":
                self.exam_preparation(filename),

            "concept_explanation":
                self.concept_explanation(filename),

        }

    # ------------------------------------------------------------------

    def health_check(self):

        return {

            "service": "Notes Service",

            "model": self.llm.get_model_name(),

            "status": "Running",

        }


notes_service = NotesService()
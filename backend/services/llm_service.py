"""
File: backend/services/llm_service.py
"""
import base64
from pathlib import Path
from typing import List, Optional

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI

from core.config import settings
from core.logger import logger


class LLMService:
    """
    Centralized Gemini LLM Service.

    All AI interactions should go through this class.

    Used by:

    - RAG Service
    - Summarization Service
    - Comparison Service
    - Notes Service
    - Image Service
    """

    _instance = None
    _llm = None

    # ----------------------------------------------------------

    def __new__(cls):

        if cls._instance is None:
            cls._instance = super().__new__(cls)

        return cls._instance

    # ----------------------------------------------------------

    def __init__(self):

        if self._llm is None:

            logger.info(
                "Initializing Gemini Model..."
            )

            self._llm = ChatGoogleGenerativeAI(
                model=settings.GEMINI_MODEL,
                google_api_key=settings.GEMINI_API_KEY,
                temperature=settings.TEMPERATURE,
                max_output_tokens=settings.MAX_OUTPUT_TOKENS,
            )

            logger.info(
                "Gemini initialized successfully."
            )

    # ----------------------------------------------------------

    @property
    def model(self):

        return self._llm

    # ----------------------------------------------------------

    def invoke(
        self,
        system_prompt: str,
        user_prompt: str,
    ) -> str:
        """
        Standard text generation.
        """

        messages = [

            SystemMessage(
                content=system_prompt,
            ),

            HumanMessage(
                content=user_prompt,
            ),
        ]

        response = self._llm.invoke(
            messages
        )

        return response.content

    # ----------------------------------------------------------

    async def ainvoke(
        self,
        system_prompt: str,
        user_prompt: str,
    ) -> str:
        """
        Async text generation.
        """

        messages = [

            SystemMessage(
                content=system_prompt,
            ),

            HumanMessage(
                content=user_prompt,
            ),
        ]

        response = await self._llm.ainvoke(
            messages
        )

        return response.content

    # ----------------------------------------------------------

    def invoke_multimodal(
        self,
        image_path: Path,
        prompt: str,
    ) -> str:

        with open(image_path, "rb") as image_file:
            image_data = base64.b64encode(
                image_file.read()
            ).decode("utf-8")

        message = HumanMessage(
            content=[
                {
                    "type": "text",
                    "text": prompt,
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{image_data}"
                    },
                },
            ]
        )

        response = self._llm.invoke(
            [message]
        )

        return response.content
    # ----------------------------------------------------------

    def batch_generate(
        self,
        prompts: List[str],
        system_prompt: Optional[str] = None,
    ) -> List[str]:
        """
        Batch inference.
        """

        responses = []

        for prompt in prompts:

            if system_prompt:

                response = self.invoke(
                    system_prompt,
                    prompt,
                )

            else:

                response = self._llm.invoke(
                    prompt
                ).content

            responses.append(
                response
            )

        return responses

    # ----------------------------------------------------------

    def get_model_name(
        self,
    ) -> str:

        return settings.GEMINI_MODEL


llm_service = LLMService()
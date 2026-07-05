"""
File: backend/api/summarize.py
"""

from fastapi import APIRouter, HTTPException

from core.logger import logger
from models.request_models import SummarizeRequest
from models.response_models import AIResponse
from services.summarization_service import summarization_service

router = APIRouter(
    prefix="/summarize",
    tags=["Summarization"],
)


# ============================================================================
# Complete Summary
# ============================================================================

@router.post(
    "",
    response_model=AIResponse,
)
async def summarize_document(
    request: SummarizeRequest,
):
    """
    Generate complete document summary.
    """

    try:

        response = summarization_service.summarize(
            filename=request.filename,
        )

        return AIResponse(
            success=True,
            message="Summary generated successfully.",
            response=response,
        )

    except Exception as error:

        logger.exception(error)

        raise HTTPException(
            status_code=500,
            detail=str(error),
        )


# ============================================================================
# Executive Summary
# ============================================================================

@router.post(
    "/executive",
    response_model=AIResponse,
)
async def executive_summary(
    request: SummarizeRequest,
):

    try:

        response = summarization_service.executive_summary(
            filename=request.filename,
        )

        return AIResponse(
            success=True,
            message="Executive Summary generated successfully.",
            response={
                "filename": request.filename,
                "executive_summary": response,
            },
        )

    except Exception as error:

        logger.exception(error)

        raise HTTPException(
            status_code=500,
            detail=str(error),
        )


# ============================================================================
# Key Findings
# ============================================================================

@router.post(
    "/key-findings",
    response_model=AIResponse,
)
async def key_findings(
    request: SummarizeRequest,
):

    try:

        response = summarization_service.key_findings(
            filename=request.filename,
        )

        return AIResponse(
            success=True,
            message="Key Findings generated successfully.",
            response={
                "filename": request.filename,
                "key_findings": response,
            },
        )

    except Exception as error:

        logger.exception(error)

        raise HTTPException(
            status_code=500,
            detail=str(error),
        )


# ============================================================================
# Methodology
# ============================================================================

@router.post(
    "/methodology",
    response_model=AIResponse,
)
async def methodology(
    request: SummarizeRequest,
):

    try:

        response = summarization_service.methodology(
            filename=request.filename,
        )

        return AIResponse(
            success=True,
            message="Methodology generated successfully.",
            response={
                "filename": request.filename,
                "methodology": response,
            },
        )

    except Exception as error:

        logger.exception(error)

        raise HTTPException(
            status_code=500,
            detail=str(error),
        )


# ============================================================================
# Limitations
# ============================================================================

@router.post(
    "/limitations",
    response_model=AIResponse,
)
async def limitations(
    request: SummarizeRequest,
):

    try:

        response = summarization_service.limitations(
            filename=request.filename,
        )

        return AIResponse(
            success=True,
            message="Limitations generated successfully.",
            response={
                "filename": request.filename,
                "limitations": response,
            },
        )

    except Exception as error:

        logger.exception(error)

        raise HTTPException(
            status_code=500,
            detail=str(error),
        )


# ============================================================================
# Future Work
# ============================================================================

@router.post(
    "/future-work",
    response_model=AIResponse,
)
async def future_work(
    request: SummarizeRequest,
):

    try:

        response = summarization_service.future_work(
            filename=request.filename,
        )

        return AIResponse(
            success=True,
            message="Future Work generated successfully.",
            response={
                "filename": request.filename,
                "future_work": response,
            },
        )

    except Exception as error:

        logger.exception(error)

        raise HTTPException(
            status_code=500,
            detail=str(error),
        )


# ============================================================================
# Contribution
# ============================================================================

@router.post(
    "/contribution",
    response_model=AIResponse,
)
async def contribution(
    request: SummarizeRequest,
):

    try:

        response = summarization_service.contribution(
            filename=request.filename,
        )

        return AIResponse(
            success=True,
            message="Contribution generated successfully.",
            response={
                "filename": request.filename,
                "contribution": response,
            },
        )

    except Exception as error:

        logger.exception(error)

        raise HTTPException(
            status_code=500,
            detail=str(error),
        )


# ============================================================================
# Abstract
# ============================================================================

@router.post(
    "/abstract",
    response_model=AIResponse,
)
async def abstract(
    request: SummarizeRequest,
):

    try:

        response = summarization_service.abstract(
            filename=request.filename,
        )

        return AIResponse(
            success=True,
            message="Abstract generated successfully.",
            response={
                "filename": request.filename,
                "abstract": response,
            },
        )

    except Exception as error:

        logger.exception(error)

        raise HTTPException(
            status_code=500,
            detail=str(error),
        )


# ============================================================================
# One Line Summary
# ============================================================================

@router.post(
    "/one-line",
    response_model=AIResponse,
)
async def one_line_summary(
    request: SummarizeRequest,
):

    try:

        response = summarization_service.one_line_summary(
            filename=request.filename,
        )

        return AIResponse(
            success=True,
            message="One-line Summary generated successfully.",
            response={
                "filename": request.filename,
                "one_line_summary": response,
            },
        )

    except Exception as error:

        logger.exception(error)

        raise HTTPException(
            status_code=500,
            detail=str(error),
        )


# ============================================================================
# TLDR
# ============================================================================

@router.post(
    "/tldr",
    response_model=AIResponse,
)
async def tldr(
    request: SummarizeRequest,
):

    try:

        response = summarization_service.tldr(
            filename=request.filename,
        )

        return AIResponse(
            success=True,
            message="TLDR generated successfully.",
            response={
                "filename": request.filename,
                "tldr": response,
            },
        )

    except Exception as error:

        logger.exception(error)

        raise HTTPException(
            status_code=500,
            detail=str(error),
        )


# ============================================================================
# Generate Complete Summary Package
# ============================================================================

@router.post(
    "/all",
    response_model=AIResponse,
)
async def generate_all(
    request: SummarizeRequest,
):
    """
    Generate all summary types in a single request.
    """

    try:

        response = summarization_service.generate_all(
            filename=request.filename,
        )

        return AIResponse(
            success=True,
            message="Complete summary package generated successfully.",
            response=response,
        )

    except Exception as error:

        logger.exception(error)

        raise HTTPException(
            status_code=500,
            detail=str(error),
        )


# ============================================================================
# Health Check
# ============================================================================

@router.get(
    "/health",
)
async def summarization_health():
    """
    Health check endpoint.
    """

    return summarization_service.health_check()
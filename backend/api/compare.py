"""
File: backend/api/compare.py
"""

from fastapi import APIRouter, HTTPException

from core.logger import logger
from models.request_models import CompareRequest
from models.response_models import AIResponse
from services.compare_service import compare_service

router = APIRouter(
    prefix="/compare",
    tags=["Comparison"],
)


# ============================================================================
# Complete Comparison
# ============================================================================

@router.post(
    "",
    response_model=AIResponse,
)
async def compare_documents(
    request: CompareRequest,
):
    """
    Compare two research papers.
    """

    try:

        response = compare_service.compare(
            document_1=request.document_1,
            document_2=request.document_2,
        )

        return AIResponse(
            success=True,
            message="Comparison generated successfully.",
            response=response,
        )

    except Exception as error:

        logger.exception(error)

        raise HTTPException(
            status_code=500,
            detail=str(error),
        )


# ============================================================================
# Similarities
# ============================================================================

@router.post(
    "/similarities",
    response_model=AIResponse,
)
async def similarities(
    request: CompareRequest,
):

    try:

        response = compare_service.similarities(
            document_1=request.document_1,
            document_2=request.document_2,
        )

        return AIResponse(
            success=True,
            message="Similarities generated successfully.",
            response={
                "document_1": request.document_1,
                "document_2": request.document_2,
                "similarities": response,
            },
        )

    except Exception as error:

        logger.exception(error)

        raise HTTPException(
            status_code=500,
            detail=str(error),
        )


# ============================================================================
# Differences
# ============================================================================

@router.post(
    "/differences",
    response_model=AIResponse,
)
async def differences(
    request: CompareRequest,
):

    try:

        response = compare_service.differences(
            document_1=request.document_1,
            document_2=request.document_2,
        )

        return AIResponse(
            success=True,
            message="Differences generated successfully.",
            response={
                "document_1": request.document_1,
                "document_2": request.document_2,
                "differences": response,
            },
        )

    except Exception as error:

        logger.exception(error)

        raise HTTPException(
            status_code=500,
            detail=str(error),
        )


# ============================================================================
# Methodology Comparison
# ============================================================================

@router.post(
    "/methodology",
    response_model=AIResponse,
)
async def methodology(
    request: CompareRequest,
):

    try:

        response = compare_service.methodology(
            document_1=request.document_1,
            document_2=request.document_2,
        )

        return AIResponse(
            success=True,
            message="Methodology comparison generated successfully.",
            response={
                "document_1": request.document_1,
                "document_2": request.document_2,
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
# Results Comparison
# ============================================================================

@router.post(
    "/results",
    response_model=AIResponse,
)
async def results(
    request: CompareRequest,
):

    try:

        response = compare_service.results(
            document_1=request.document_1,
            document_2=request.document_2,
        )

        return AIResponse(
            success=True,
            message="Results comparison generated successfully.",
            response={
                "document_1": request.document_1,
                "document_2": request.document_2,
                "results": response,
            },
        )

    except Exception as error:

        logger.exception(error)

        raise HTTPException(
            status_code=500,
            detail=str(error),
        )


# ============================================================================
# Advantages & Limitations
# ============================================================================

@router.post(
    "/advantages-limitations",
    response_model=AIResponse,
)
async def advantages_limitations(
    request: CompareRequest,
):

    try:

        response = compare_service.advantages_limitations(
            document_1=request.document_1,
            document_2=request.document_2,
        )

        return AIResponse(
            success=True,
            message="Advantages & Limitations generated successfully.",
            response={
                "document_1": request.document_1,
                "document_2": request.document_2,
                "advantages_limitations": response,
            },
        )

    except Exception as error:

        logger.exception(error)

        raise HTTPException(
            status_code=500,
            detail=str(error),
        )


# ============================================================================
# Best Paper
# ============================================================================

@router.post(
    "/best-paper",
    response_model=AIResponse,
)
async def best_paper(
    request: CompareRequest,
):

    try:

        response = compare_service.best_paper(
            document_1=request.document_1,
            document_2=request.document_2,
        )

        return AIResponse(
            success=True,
            message="Best paper analysis generated successfully.",
            response={
                "document_1": request.document_1,
                "document_2": request.document_2,
                "best_paper": response,
            },
        )

    except Exception as error:

        logger.exception(error)

        raise HTTPException(
            status_code=500,
            detail=str(error),
        )


# ============================================================================
# Technical Comparison
# ============================================================================

@router.post(
    "/technical",
    response_model=AIResponse,
)
async def technical(
    request: CompareRequest,
):

    try:

        response = compare_service.technical_comparison(
            document_1=request.document_1,
            document_2=request.document_2,
        )

        return AIResponse(
            success=True,
            message="Technical comparison generated successfully.",
            response={
                "document_1": request.document_1,
                "document_2": request.document_2,
                "technical_comparison": response,
            },
        )

    except Exception as error:

        logger.exception(error)

        raise HTTPException(
            status_code=500,
            detail=str(error),
        )


# ============================================================================
# Comparison Table
# ============================================================================

@router.post(
    "/table",
    response_model=AIResponse,
)
async def comparison_table(
    request: CompareRequest,
):

    try:

        response = compare_service.comparison_table(
            document_1=request.document_1,
            document_2=request.document_2,
        )

        return AIResponse(
            success=True,
            message="Comparison table generated successfully.",
            response={
                "document_1": request.document_1,
                "document_2": request.document_2,
                "comparison_table": response,
            },
        )

    except Exception as error:

        logger.exception(error)

        raise HTTPException(
            status_code=500,
            detail=str(error),
        )


# ============================================================================
# Complete Comparison Package
# ============================================================================

@router.post(
    "/all",
    response_model=AIResponse,
)
async def generate_complete_comparison(
    request: CompareRequest,
):

    try:

        response = compare_service.generate_all(
            document_1=request.document_1,
            document_2=request.document_2,
        )

        return AIResponse(
            success=True,
            message="Complete comparison package generated successfully.",
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
async def health():

    return compare_service.health_check()
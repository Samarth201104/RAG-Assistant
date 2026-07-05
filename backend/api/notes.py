"""
File: backend/api/notes.py
"""

from fastapi import APIRouter, HTTPException

from core.logger import logger
from models.request_models import NotesRequest
from models.response_models import AIResponse
from services.notes_service import notes_service

router = APIRouter(
    prefix="/notes",
    tags=["Study Notes"],
)


# ============================================================================
# Generate Notes by Type
# ============================================================================

@router.post(
    "",
    response_model=AIResponse,
)
async def generate_notes(
    request: NotesRequest,
):
    """
    Generate notes based on the requested note type.
    """

    try:

        response = notes_service.generate_by_type(
            filename=request.filename,
            note_type=request.note_type,
        )

        return AIResponse(
            success=True,
            message=f"{request.note_type.title()} generated successfully.",
            response=response,
        )

    except Exception as error:

        logger.exception(error)

        raise HTTPException(
            status_code=500,
            detail=str(error),
        )


# ============================================================================
# Short Notes
# ============================================================================

@router.post(
    "/short",
    response_model=AIResponse,
)
async def short_notes(
    request: NotesRequest,
):

    try:

        response = notes_service.short_notes(
            filename=request.filename,
        )

        return AIResponse(
            success=True,
            message="Short Notes generated successfully.",
            response={
                "filename": request.filename,
                "short_notes": response,
            },
        )

    except Exception as error:

        logger.exception(error)

        raise HTTPException(
            status_code=500,
            detail=str(error),
        )


# ============================================================================
# Detailed Notes
# ============================================================================

@router.post(
    "/detailed",
    response_model=AIResponse,
)
async def detailed_notes(
    request: NotesRequest,
):

    try:

        response = notes_service.detailed_notes(
            filename=request.filename,
        )

        return AIResponse(
            success=True,
            message="Detailed Notes generated successfully.",
            response={
                "filename": request.filename,
                "detailed_notes": response,
            },
        )

    except Exception as error:

        logger.exception(error)

        raise HTTPException(
            status_code=500,
            detail=str(error),
        )


# ============================================================================
# Flashcards
# ============================================================================

@router.post(
    "/flashcards",
    response_model=AIResponse,
)
async def flashcards(
    request: NotesRequest,
):

    try:

        response = notes_service.flashcards(
            filename=request.filename,
        )

        return AIResponse(
            success=True,
            message="Flashcards generated successfully.",
            response={
                "filename": request.filename,
                "flashcards": response,
            },
        )

    except Exception as error:

        logger.exception(error)

        raise HTTPException(
            status_code=500,
            detail=str(error),
        )


# ============================================================================
# Interview Questions
# ============================================================================

@router.post(
    "/interview",
    response_model=AIResponse,
)
async def interview_questions(
    request: NotesRequest,
):

    try:

        response = notes_service.interview_questions(
            filename=request.filename,
        )

        return AIResponse(
            success=True,
            message="Interview Questions generated successfully.",
            response={
                "filename": request.filename,
                "interview_questions": response,
            },
        )

    except Exception as error:

        logger.exception(error)

        raise HTTPException(
            status_code=500,
            detail=str(error),
        )


# ============================================================================
# Viva Questions
# ============================================================================

@router.post(
    "/viva",
    response_model=AIResponse,
)
async def viva_questions(
    request: NotesRequest,
):

    try:

        response = notes_service.viva_questions(
            filename=request.filename,
        )

        return AIResponse(
            success=True,
            message="Viva Questions generated successfully.",
            response={
                "filename": request.filename,
                "viva_questions": response,
            },
        )

    except Exception as error:

        logger.exception(error)

        raise HTTPException(
            status_code=500,
            detail=str(error),
        )


# ============================================================================
# MCQs
# ============================================================================

@router.post(
    "/mcq",
    response_model=AIResponse,
)
async def mcqs(
    request: NotesRequest,
):

    try:

        response = notes_service.mcqs(
            filename=request.filename,
        )

        return AIResponse(
            success=True,
            message="MCQs generated successfully.",
            response={
                "filename": request.filename,
                "mcqs": response,
            },
        )

    except Exception as error:

        logger.exception(error)

        raise HTTPException(
            status_code=500,
            detail=str(error),
        )


# ============================================================================
# Revision Notes
# ============================================================================

@router.post(
    "/revision",
    response_model=AIResponse,
)
async def revision_notes(
    request: NotesRequest,
):

    try:

        response = notes_service.revision_notes(
            filename=request.filename,
        )

        return AIResponse(
            success=True,
            message="Revision Notes generated successfully.",
            response={
                "filename": request.filename,
                "revision_notes": response,
            },
        )

    except Exception as error:

        logger.exception(error)

        raise HTTPException(
            status_code=500,
            detail=str(error),
        )


# ============================================================================
# Cheat Sheet
# ============================================================================

@router.post(
    "/cheatsheet",
    response_model=AIResponse,
)
async def cheat_sheet(
    request: NotesRequest,
):

    try:

        response = notes_service.cheat_sheet(
            filename=request.filename,
        )

        return AIResponse(
            success=True,
            message="Cheat Sheet generated successfully.",
            response={
                "filename": request.filename,
                "cheat_sheet": response,
            },
        )

    except Exception as error:

        logger.exception(error)

        raise HTTPException(
            status_code=500,
            detail=str(error),
        )


# ============================================================================
# Mind Map
# ============================================================================

@router.post(
    "/mindmap",
    response_model=AIResponse,
)
async def mind_map(
    request: NotesRequest,
):

    try:

        response = notes_service.mind_map(
            filename=request.filename,
        )

        return AIResponse(
            success=True,
            message="Mind Map generated successfully.",
            response={
                "filename": request.filename,
                "mind_map": response,
            },
        )

    except Exception as error:

        logger.exception(error)

        raise HTTPException(
            status_code=500,
            detail=str(error),
        )


# ============================================================================
# FAQ
# ============================================================================

@router.post(
    "/faq",
    response_model=AIResponse,
)
async def faq(
    request: NotesRequest,
):

    try:

        response = notes_service.faqs(
            filename=request.filename,
        )

        return AIResponse(
            success=True,
            message="FAQs generated successfully.",
            response={
                "filename": request.filename,
                "faqs": response,
            },
        )

    except Exception as error:

        logger.exception(error)

        raise HTTPException(
            status_code=500,
            detail=str(error),
        )


# ============================================================================
# Exam Preparation
# ============================================================================

@router.post(
    "/exam",
    response_model=AIResponse,
)
async def exam_preparation(
    request: NotesRequest,
):

    try:

        response = notes_service.exam_preparation(
            filename=request.filename,
        )

        return AIResponse(
            success=True,
            message="Exam Preparation generated successfully.",
            response={
                "filename": request.filename,
                "exam_preparation": response,
            },
        )

    except Exception as error:

        logger.exception(error)

        raise HTTPException(
            status_code=500,
            detail=str(error),
        )


# ============================================================================
# Concept Explanation
# ============================================================================

@router.post(
    "/concept",
    response_model=AIResponse,
)
async def concept_explanation(
    request: NotesRequest,
):

    try:

        response = notes_service.concept_explanation(
            filename=request.filename,
        )

        return AIResponse(
            success=True,
            message="Concept Explanation generated successfully.",
            response={
                "filename": request.filename,
                "concept_explanation": response,
            },
        )

    except Exception as error:

        logger.exception(error)

        raise HTTPException(
            status_code=500,
            detail=str(error),
        )


# ============================================================================
# Generate Complete Study Package
# ============================================================================

@router.post(
    "/all",
    response_model=AIResponse,
)
async def generate_complete_notes(
    request: NotesRequest,
):

    try:

        response = notes_service.generate_all(
            filename=request.filename,
        )

        return AIResponse(
            success=True,
            message="Complete Study Package generated successfully.",
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

    return notes_service.health_check()
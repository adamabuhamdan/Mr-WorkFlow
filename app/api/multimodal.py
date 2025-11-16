from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from pydantic import BaseModel

from app.services.llm_service import LLMService

router = APIRouter()

llm_service = LLMService()


class ImageChatResponse(BaseModel):
    answer: str
    success: bool

class FileChatResponse(BaseModel):
    answer: str
    success: bool

@router.post("/chat-with-image", response_model=ImageChatResponse)
async def chat_with_image(
    question: str = Form(...),
    language: str = Form("en"),
    image: UploadFile = File(...),
) -> ImageChatResponse:
    """Multimodal chat endpoint: question + image.

    The client sends:
    - question: user question (form field)
    - language: "en" or "ar" (form field)
    - image: uploaded image file (JPEG/PNG/...)."""

    if language not in {"en", "ar"}:
        raise HTTPException(
            status_code=400,
            detail="Language must be either 'en' or 'ar'.",
        )

    if not image.content_type or not image.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400,
            detail="Uploaded file must be an image (jpeg, png, ...).",
        )

    try:
        image_bytes = await image.read()
    except Exception as e:  # noqa: BLE001
        raise HTTPException(
            status_code=400,
            detail=f"Failed to read uploaded image: {e}",
        ) from e

    result = llm_service.generate_response_with_image(
        question=question,
        image_bytes=image_bytes,
        mime_type=image.content_type,
        language=language,
    )

    return ImageChatResponse(
        answer=result.get("answer", ""),
        success=result.get("success", False),
    )

@router.post("/chat-with-file", response_model=FileChatResponse)
async def chat_with_file(
    question: str = Form(...),
    language: str = Form("en"),
    file: UploadFile = File(...),
) -> FileChatResponse:
    """Multimodal chat endpoint: question + file.

    The client sends:
    - question: user question (form field)
    - language: "en" or "ar" (form field)
    - file: uploaded document (PDF, markdown, text, etc.).
    """

    if language not in {"en", "ar"}:
        raise HTTPException(
            status_code=400,
            detail="Language must be either 'en' or 'ar'.",
        )

    if not file.content_type:
        raise HTTPException(
            status_code=400,
            detail="Uploaded file must have a valid content type.",
        )

    # Optionally, you can restrict allowed types (for now we allow most text/PDF types)
    allowed_prefixes = ("application/pdf", "text/", "application/vnd.openxmlformats")
    if not file.content_type.startswith(allowed_prefixes):
        # Not blocking hard, but you can tighten this logic if needed
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type: {file.content_type}. "
            "Please upload a PDF or text-based document.",
        )

    try:
        file_bytes = await file.read()
    except Exception as e:  # noqa: BLE001
        raise HTTPException(
            status_code=400,
            detail=f"Failed to read uploaded file: {e}",
        ) from e

    result = llm_service.generate_response_with_file(
        question=question,
        file_bytes=file_bytes,
        filename=file.filename or "uploaded_file",
        mime_type=file.content_type,
        language=language,
    )

    return FileChatResponse(
        answer=result.get("answer", ""),
        success=result.get("success", False),
    )


@router.get("/multimodal/health")
async def multimodal_health() -> dict:
    """Simple health check for the multimodal endpoints."""
    return {"status": "healthy", "service": "startup_advisor_multimodal"}

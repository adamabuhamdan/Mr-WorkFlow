from typing import List, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.llm_service import LLMService
from app.services.vector_store import VectorStoreService

router = APIRouter()


class ChatRequest(BaseModel):
    question: str
    language: str = "en"  # "en" or "ar"
    # If True, Gemini will auto-detect relevant stages from the question.
    # If False, the backend will search across all stages.
    auto_stage_detection: bool = True
    # Optional manual override: if provided and auto_stage_detection=False,
    # the search will be restricted to these stages.
    stages: Optional[List[str]] = None


class ChatResponse(BaseModel):
    answer: str
    sources: List[str]
    context_used: int
    success: bool
    detected_stages: List[str]


# Initialize shared services
vector_service = VectorStoreService()
llm_service = LLMService()


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    """Main chat endpoint used by the frontend."""
    try:
        if request.language not in {"en", "ar"}:
            raise HTTPException(
                status_code=400,
                detail="Language must be either 'en' or 'ar'.",
            )

        detected_stages: List[str] = []

        # Decide which stages to use for retrieval
        if request.auto_stage_detection:
            detected_stages = llm_service.detect_stages(request.question)
            # It is okay if this returns an empty list: we will fall back to global search.
        else:
            if request.stages:
                detected_stages = request.stages

        # Retrieve relevant context from the vector store
        similar_docs = vector_service.search_similar(
            query=request.question,
            limit=5,
            stages=detected_stages if detected_stages else None,
        )

        if not similar_docs:
            message = (
                "Sorry, I could not find enough relevant information to answer your "
                "question. Please try another question related to entrepreneurship or "
                "startup building."
            )
            return ChatResponse(
                answer=message,
                sources=[],
                context_used=0,
                success=False,
                detected_stages=detected_stages,
            )

        # Let the LLM generate the final answer
        response_data = llm_service.generate_response(
            question=request.question,
            context_documents=similar_docs,
            language=request.language,
        )

        return ChatResponse(
            answer=response_data["answer"],
            sources=response_data["sources"],
            context_used=response_data["context_used"],
            success=True,
            detected_stages=detected_stages,
        )

    except HTTPException:
        raise
    except Exception as e:  # noqa: BLE001
        raise HTTPException(
            status_code=500,
            detail=f"Error processing request: {e}",
        ) from e


@router.get("/health")
async def health_check() -> dict:
    """Simple health check endpoint."""
    return {"status": "healthy", "service": "startup_advisor_ai"}

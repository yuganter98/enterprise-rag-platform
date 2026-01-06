from typing import Any
from fastapi import APIRouter, Depends
from app.api import deps
from app.models.user import User
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.rag.chat import answer_question

router = APIRouter()

@router.post("/", response_model=ChatResponse)
def chat(
    request: ChatRequest,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Chat with the AI assistant.
    The answer is generating using RAG based on the user's role.
    """
    # Pass user's role name to the RAG service for filtering
    role_name = current_user.role.name if current_user.role else "employee"
    
    response_text = answer_question(request.query, role=role_name)
    return {"response": response_text}

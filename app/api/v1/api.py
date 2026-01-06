from fastapi import APIRouter
from app.api.v1.endpoints import auth, chat, documents, reports, email, events, users

api_router = APIRouter()

api_router.include_router(auth.router, tags=["login"])
api_router.include_router(chat.router, prefix="/chat", tags=["chat"])
api_router.include_router(documents.router, prefix="/documents", tags=["documents"])
api_router.include_router(reports.router, prefix="/reports", tags=["reports"])
api_router.include_router(email.router, prefix="/email", tags=["email"])
api_router.include_router(events.router, prefix="/events", tags=["events"])
api_router.include_router(users.router, prefix="/users", tags=["users"])

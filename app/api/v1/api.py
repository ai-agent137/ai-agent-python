from fastapi import APIRouter

from app.api.v1.chat import router as chat_router
from app.api.v1.conversations import router as conversations_router
from app.api.v1.health import router as health_router
from app.api.v1.rag import router as rag_router
from app.api.v1.models import router as models_router
from app.core.constants import ApiTag


api_router = APIRouter()

api_router.include_router(health_router, tags=[ApiTag.HEALTH])
api_router.include_router(chat_router, tags=[ApiTag.CHAT])
api_router.include_router(conversations_router, tags=[ApiTag.CONVERSATIONS])
api_router.include_router(rag_router, tags=[ApiTag.RAG])
api_router.include_router(models_router, tags=[ApiTag.MODELS])
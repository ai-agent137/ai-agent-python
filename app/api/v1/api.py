from fastapi import APIRouter, Depends

from app.api.v1.chat import router as chat_router
from app.api.v1.conversations import router as conversations_router
from app.api.v1.health import router as health_router
from app.api.v1.rag import router as rag_router
from app.api.v1.models import router as models_router
from app.api.v1.agents import router as agent_router
from app.core.constants import ApiTag
from app.dependencies.auth import verify_api_key
from app.api.v1.prompts import router as prompts_router


api_router = APIRouter()

api_router.include_router(health_router, tags=[ApiTag.HEALTH])
api_router.include_router(models_router, tags=[ApiTag.MODELS])

api_router.include_router(chat_router, tags=[ApiTag.CHAT],dependencies=[Depends(verify_api_key)])
api_router.include_router(conversations_router, tags=[ApiTag.CONVERSATIONS],dependencies=[Depends(verify_api_key)])
api_router.include_router(rag_router, tags=[ApiTag.RAG],dependencies=[Depends(verify_api_key)])
api_router.include_router(agent_router, tags=[ApiTag.AGENTS],dependencies=[Depends(verify_api_key)])
api_router.include_router(prompts_router, tags=["Prompts"])
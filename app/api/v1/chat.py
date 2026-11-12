from typing import AsyncGenerator
from fastapi import APIRouter, Depends, Path, Query, Body, Request
from fastapi.responses import StreamingResponse
from redis.asyncio import Redis
from app.dependencies.auth import get_current_user
from app.dependencies.database import get_db_session
from app.dependencies.llm import get_llm_provider
from app.dependencies.rate_limit import chat_rate_limit
from app.dependencies.redis import get_redis_client
from app.llm.base import BaseLLMProvider
from app.schema.chat import ChatRequest
from app.schema.conversation import ConversationMessagesResponse
from app.schema.response import ApiResponse
from app.schema.user import CurrentUser
from app.service.chat_service import chat_with_ai
from app.schema.chat import ChatResponse, GenerateTitleRequest,GenerateTitleResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.service.chat_stream_service import stream_chat_with_ai
from app.service.conversation_service import get_conversation_messages
router = APIRouter()


@router.post(
    "/chat/stream",
    dependencies=[Depends(chat_rate_limit)]
)
async def chat_steam(
    request_body: ChatRequest,
    request: Request,
    current_user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
    redis: Redis = Depends(get_redis_client),
    llm_provider: BaseLLMProvider = Depends(get_llm_provider),
):
    async def event_generator():
        async for event in stream_chat_with_ai(
            request=request_body,
            llm_provider=llm_provider,
            db=db,
            redis=redis
        ):
            # 判断页面是否关闭 
            if await request.is_disconnected():
                break
            yield event
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no" # 避免某些反向代理缓冲响应
        },
    )        
    

@router.post(
        "/chat", 
        response_model=ApiResponse[ChatResponse],
        dependencies=[Depends(chat_rate_limit)]
        )
async def chat_endpoint(
    request: ChatRequest,
    db: AsyncSession = Depends(get_db_session),
    current_user: CurrentUser = Depends(get_current_user),
    redis: Redis = Depends(get_redis_client),
    llm_provider: BaseLLMProvider = Depends(get_llm_provider),
    ):
    result =  await chat_with_ai(
        request=request,
         db=db,
         redis=redis,
         llm_provider=llm_provider
        )
    result.trace_id = f"{result.trace_id}_user_{current_user.user_id}"
    return ApiResponse[ChatResponse](data=result)




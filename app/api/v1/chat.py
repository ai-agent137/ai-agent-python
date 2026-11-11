from fastapi import APIRouter, Depends, Path, Query, Body
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
from app.service.conversation_service import get_conversation_messages
router = APIRouter()

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



@router.post("/chat/title", response_model=ApiResponse[GenerateTitleResponse])
async def generate_chat_title(
    request: GenerateTitleRequest,
) -> ApiResponse[GenerateTitleResponse]:
    title = request.message[:20]

    return ApiResponse[GenerateTitleResponse](
        data=GenerateTitleResponse(title=title)
    )



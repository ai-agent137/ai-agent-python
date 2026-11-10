from fastapi import APIRouter, Depends, Path
from redis import Redis
from app.dependencies.auth import get_current_user
from app.dependencies.database import get_db_session
from app.dependencies.pagination import PaginationParams
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.redis import get_redis_client
from app.schema.conversation import (
    ConversationCreateRequest,
    ConversationMessagesResponse,
    ConversationResponse,
)
from app.schema.response import ApiResponse
from app.schema.user import CurrentUser
from app.service.conversation_service import (
    create_conversation,
    get_conversation_messages,
)

router = APIRouter()


@router.post("/conversations", response_model=ApiResponse[ConversationResponse])
async def create_new_conversation(
    request: ConversationCreateRequest,
    db: AsyncSession = Depends(get_db_session),
    current_user: CurrentUser = Depends(get_current_user),
) -> ApiResponse[dict]:

    result = await create_conversation(
        db=db,
        request=request,
        user_id=current_user.user_id,
    )

    return ApiResponse[ConversationResponse](
        data=result
    )


@router.get(
    "/conversations/{conversation_id}/messages",
    response_model=ApiResponse[ConversationMessagesResponse],
)
async def get_messages(
    conversation_id: str = Path(..., description="会话 ID"),
    db: AsyncSession = Depends(get_db_session),
    redis: Redis = Depends(get_redis_client)
) -> ApiResponse[ConversationMessagesResponse]:
    result = await get_conversation_messages(
        db=db,
        conversation_id=conversation_id,
        redis=redis
    )

    return ApiResponse[ConversationMessagesResponse](
        data=result
    )


@router.get("/conversations", response_model=ApiResponse[dict])
async def list_conversations(
    pagination: PaginationParams = Depends(PaginationParams),
) -> ApiResponse[dict]:
    return ApiResponse[dict](
        data={
            "page": pagination.page,
            "page_size": pagination.page_size,
            "offset": pagination.offset,
            "items": [],
        }
    )
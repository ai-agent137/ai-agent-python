import uuid

from redis import Redis
from app.redis.cache import cache_recent_messages, get_cached_recent_messages

from app.schema.chat import ChatMessage, MessageRole
from app.schema.conversation import (
    ConversationCreateRequest,
    ConversationMessagesResponse,
    ConversationResponse,
)
from app.repositories.conversation_repository import conversation_repository

from sqlalchemy.ext.asyncio import AsyncSession

async def create_conversation(
    db: AsyncSession,
    request: ConversationCreateRequest,
    user_id: str | None = None,
) -> ConversationResponse:
    conversation = await conversation_repository.create(
        db=db,
        request=request,
        user_id=user_id,
    )
    return ConversationResponse(
        conversation_id=conversation.id,
        title=conversation.title,
        status=conversation.status,
        created_at=conversation.created_at,
        updated_at=conversation.updated_at,
    )


async def get_conversation_messages(
    db: AsyncSession,
    conversation_id: str,
    redis: Redis | None = None
) -> ConversationMessagesResponse:
    if redis:
        cache_messages = await get_cached_recent_messages(
            redis = redis,
            conversation_id = conversation_id
        )
        if cache_messages is not None:
            return ConversationMessagesResponse(
                conversation_id=conversation_id,
                messages=cache_messages
            )
    
    messages = await conversation_repository.get_messages(
        db=db,
        conversation_id=conversation_id,
    )

    # 缓存10条    
    if redis:
        await cache_recent_messages(
            redis=redis,
            conversation_id=conversation_id,
            messages=messages[-10:],
        )

    return ConversationMessagesResponse(
        conversation_id=conversation_id,
        messages=messages,
    )
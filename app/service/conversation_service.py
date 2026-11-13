import uuid

from redis import Redis
from app.core.exceptions import AppException, ErrorCode
from app.redis.cache import cache_recent_messages, get_cached_recent_messages

from app.schema.chat import ChatMessage, MessageRole
from app.schema.conversation import (
    ConversationCreateRequest,
    ConversationListResponse,
    ConversationMessagesResponse,
    ConversationResponse,
    ConversationStatus,
)
from app.repositories.conversation_repository import conversation_repository

from sqlalchemy.ext.asyncio import AsyncSession
class ConversationService:
    async def create_conversation(
        self,
        db: AsyncSession,
        request: ConversationCreateRequest,
        user_id: str | None = None,
    ) -> ConversationResponse:
        conversation = await conversation_repository.create_conversation(
            db=db,
            title=request.title,
            user_id=user_id,
        )
        return ConversationResponse(
            conversation_id=conversation.id,
            title=conversation.title,
            status=conversation.status,
            created_at=conversation.created_at,
            updated_at=conversation.updated_at,
        )

    async def list_conversations(
            self,
            db: AsyncSession,
            user_id: str | None = None,
            limit: int = 20,
        ) -> ConversationListResponse:
            conversations = await conversation_repository.list_conversations(
                db=db,
                user_id=user_id,
                limit=limit,
            )

            return ConversationListResponse(
                conversations=[
                    self._to_response(conversation)
                    for conversation in conversations
                ]
            )
    async def get_conversation(
            self,
            db: AsyncSession,
            conversation_id: str,
        ) -> ConversationResponse:
            conversation = await conversation_repository.get_conversation(
                db=db,
                conversation_id=conversation_id,
            )

            if not conversation:
                raise AppException(
                    message="会话不存在",
                    code=ErrorCode.NOT_FOUND,
                    status_code=404,
                )

            return self._to_response(conversation)


    async def get_conversation_messages(
        self,
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
    def _to_response(self, conversation) -> ConversationResponse:
        return ConversationResponse(
            conversation_id=conversation.id,
            title=conversation.title,
            status=ConversationStatus(conversation.status),
            created_at=conversation.created_at,
            updated_at=conversation.updated_at,
        )    
conversation_service = ConversationService()

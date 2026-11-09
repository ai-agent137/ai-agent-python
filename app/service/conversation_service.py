import uuid

from app.schema.chat import ChatMessage, MessageRole
from app.schema.conversation import (
    ConversationCreateRequest,
    ConversationMessagesResponse,
    ConversationResponse,
)
from app.repositories.conversation_repository import conversation_respository

from app.repositories.knowledge_repository import knowledge_repository
from app.schema.chat import TokenUsage


async def create_conversation(
    request: ConversationCreateRequest,
) -> ConversationResponse:
    conversation_id=f"c_{uuid.uuid4().hex[:8]}"
    conversation = await conversation_respository.create(
        conversation_id=conversation_id,
        request=request,
    )
    return ConversationResponse(
        conversation_id=f"c_{uuid.uuid4().hex[:8]}",
        title=request.title,
    )


async def get_conversation_messages(
    conversation_id: str,
) -> ConversationMessagesResponse:
    return ConversationMessagesResponse(
        conversation_id=conversation_id,
        messages=[
            ChatMessage(
                role=MessageRole.USER,
                content="什么是 AI Agent？"
            ),
            ChatMessage(
                role=MessageRole.ASSISTANT,
                content="AI Agent 是能够调用工具完成任务的智能体。"
            )
        ]
    )
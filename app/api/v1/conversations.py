from fastapi import APIRouter, Path

from app.schema.conversation import (
    ConversationCreateRequest,
    ConversationMessagesResponse,
    ConversationResponse,
)
from app.schema.response import Response
from app.service.conversation_service import (
    create_conversation,
    get_conversation_messages,
)

router = APIRouter()


@router.post("/conversations", response_model=Response[ConversationResponse])
async def create_new_conversation(
    request: ConversationCreateRequest,
) -> Response[ConversationResponse]:
    result = await create_conversation(request)

    return Response[ConversationResponse](
        data=result
    )


@router.get(
    "/conversations/{conversation_id}/messages",
    response_model=Response[ConversationMessagesResponse],
)
async def get_messages(
    conversation_id: str = Path(..., description="会话 ID"),
) -> Response[ConversationMessagesResponse]:
    result = await get_conversation_messages(conversation_id)

    return Response[ConversationMessagesResponse](
        data=result
    )
from fastapi import APIRouter, Depends, Path
from app.dependencies.database import MockDBSession, get_db_session
from app.dependencies.pagination import PaginationParams

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
    db: MockDBSession = Depends(get_db_session),
    pagination: PaginationParams = Depends(PaginationParams)
) -> Response[dict]:
    sql_result= await db.execute("INSERT INTO conversations ...")
    print(sql_result)

    result = await create_conversation(request)

    return Response[dict](
        data={
            page: pagination.page,
            pageSize: pagination.pageSize,
            offset: pagination.offset,
            list: result
        }
    )


@router.get(
    "/conversations/{conversation_id}/messages",
    response_model=Response[ConversationMessagesResponse],
)
async def get_messages(
    conversation_id: str = Path(..., description="会话 ID")
) -> Response[ConversationMessagesResponse]:
    result = await get_conversation_messages(conversation_id)


    return Response[ConversationMessagesResponse](
        data=result
    )
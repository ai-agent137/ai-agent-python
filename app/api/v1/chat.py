from fastapi import APIRouter, Path, Query, Body
from app.schema.chat import ChatRequest
from app.schema.response import Response
from app.service.chat_service import chat_with_ai
from app.schema.chat import ChatResponse, GenerateTitleRequest,GenerateTitleResponse

router = APIRouter()

@router.post("/chat", response_model=Response[ChatResponse])
async def chat_endpoint(request: ChatRequest):
    result =  await chat_with_ai(request)
    return Response[ChatResponse](data=result)

@router.post("/conversations/{conversation_id}/chat")
async def chat_conversation_endpoint (
    request: ChatRequest,
    conversation_id: str = Path(..., description="会话 ID"),
    debug: bool = Query(False, description="是否开启调试模式"),
) -> Response[ChatResponse]:
    # 将会话 ID 添加到请求中
    request.session_id = conversation_id
    result = await chat_with_ai(request)
    if debug:
        result.trace_id = result.trace_id or "debug_trace"

    result.session_id = conversation_id    
    return Response[ChatResponse](data=result)

@router.post("/chat/title", response_model=Response[GenerateTitleResponse])
async def generate_chat_title(
    request: GenerateTitleRequest,
) -> Response[GenerateTitleResponse]:
    title = request.message[:20]

    return Response[GenerateTitleResponse](
        data=GenerateTitleResponse(title=title)
    )
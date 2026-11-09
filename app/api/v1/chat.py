from fastapi import APIRouter, Depends, Path, Query, Body
from app.dependencies.auth import get_current_user
from app.dependencies.llm import MockLLMProvider, get_llm_provider
from app.schema.chat import ChatRequest
from app.schema.response import ApiResponse
from app.schema.user import CurrentUser
from app.service.chat_service import chat_with_ai
from app.schema.chat import ChatResponse, GenerateTitleRequest,GenerateTitleResponse

router = APIRouter()

@router.post("/chat", response_model=ApiResponse[ChatResponse])
async def chat_endpoint(
    request: ChatRequest,
    current_user: CurrentUser = Depends(get_current_user)
    ):
    result =  await chat_with_ai(request)
    result.trace_id = f"{result.trace_id}_user_{current_user.user_id}"
    return ApiResponse[ChatResponse](data=result)

@router.post("/conversations/{conversation_id}/chat")
async def chat_conversation_endpoint (
    request: ChatRequest,
    conversation_id: str = Path(..., description="会话 ID"),
    debug: bool = Query(False, description="是否开启调试模式"),
) -> ApiResponse[ChatResponse]:
    # 将会话 ID 添加到请求中
    request.session_id = conversation_id
    result = await chat_with_ai(request)
    if debug:
        result.trace_id = result.trace_id or "debug_trace"

    result.session_id = conversation_id    
    return ApiResponse[ChatResponse](data=result)

@router.post("/chat/title", response_model=ApiResponse[GenerateTitleResponse])
async def generate_chat_title(
    request: GenerateTitleRequest,
) -> ApiResponse[GenerateTitleResponse]:
    title = request.message[:20]

    return ApiResponse[GenerateTitleResponse](
        data=GenerateTitleResponse(title=title)
    )

@router.post("/chat/di-demo")
async def chat_di_demo(
    request: ChatRequest,
    current_user: CurrentUser = Depends(get_current_user),
    llm_provider: MockLLMProvider = Depends(get_llm_provider)
) -> ApiResponse[ChatResponse]:
    latest_message = request.messages[-1].content
    answer = await llm_provider.chat(
        message=f"用户{current_user.username} 问: { latest_message}"
    )
    result = ChatResponse(
        answer=answer,
        model=llm_provider.model,
        session_id=request.session_id
    )
    return ApiResponse[ChatResponse](
        data=result
    )

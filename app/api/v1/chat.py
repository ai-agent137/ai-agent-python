from fastapi import APIRouter
from app.schema.chat import ChatRequest
from app.schema.response import Response
from app.service.chat_service import chat_with_ai
from app.schema.chat import ChatResponse

router = APIRouter()

@router.post("/chat", response_model=Response)
async def chat_endpoint(request: ChatRequest):
    result =  await chat_with_ai(request)
    return Response[ChatResponse](data=result)

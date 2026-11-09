import asyncio
import uuid

from app.schema.chat import (
    ChatRequest,
    ChatResponse,
    MessageRole,
    SourceDocument,
    TokenUsage,
)
from app.core.config import settings
from fastapi import HTTPException, status


async def chat_with_ai(request: ChatRequest) -> ChatResponse:
    await asyncio.sleep(0.5)

    latest_user_message = get_latest_user_message(request)
    model = request.model or settings.default_model

    if "AI Agent" in latest_user_message:
        answer = "AI Agent 是能够理解目标、规划步骤、调用工具并根据结果完成任务的智能体。"
    elif "RAG" in latest_user_message:
        answer = "RAG 是检索增强生成，用于让大模型结合企业私有知识库进行回答。"
    elif "LangGraph" in latest_user_message:
        answer = "LangGraph 适合开发有状态、有分支、有流程控制的复杂 Agent。"
    else:
        answer = f"这是一个模拟回答：你刚才问的是「{latest_user_message}」。"

    usage = TokenUsage(
        prompt_tokens=count_mock_tokens_from_messages(request),
        completion_tokens=len(answer),
        total_tokens=count_mock_tokens_from_messages(request) + len(answer),
    )

    sources = build_mock_sources(latest_user_message)

    return ChatResponse(
        answer = answer,
        model= model,
        session_id=request.session_id or f"s_{uuid.uuid4().hex[:8]}",
        message_id=f"m_{uuid.uuid4().hex[:8]}",
        usage=usage,
        sources=sources,
        trace_id=f"trace_{uuid.uuid4().hex[:8]}",
    )


def get_latest_user_message(request: ChatRequest) -> str:
    for message in reversed(request.messages):
        if message.role == MessageRole.USER:
            return message.content

    return request.messages[-1].content


def count_mock_tokens_from_messages(request: ChatRequest) -> int:
    return sum(len(message.content) for message in request.messages)


def build_mock_sources(question: str) -> list[SourceDocument]:
    if "RAG" not in question and "知识库" not in question:
        return []

    return [
        SourceDocument(
            document_id="doc_001",
            title="企业知识库说明文档",
            content="RAG 是 Retrieval Augmented Generation，用于结合外部知识增强大模型回答。",
            score=0.89,
            metadata={
                "source": "mock",
                "page": 1,
            },
        )
    ]
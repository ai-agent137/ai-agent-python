import asyncio
import uuid

from redis.asyncio import Redis
from app.core.logging import get_logger
from app.llm.base import BaseLLMProvider
from app.llm.errors import LLMProviderError
from app.llm.factory import LLMProviderFactory
from app.llm.schemas import LLMMessage, LLMRequest, LLMRole
from app.redis.cache import cache_chat_response, get_cached_chat_response
from app.schema.chat import (
    ChatRequest,
    ChatResponse,
    MessageRole,
    SourceDocument,
    TokenUsage,
)
from app.core.config import settings
from app.core.exceptions import AppException, ErrorCode
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.conversation_repository import conversation_repository
from app.prompts.base import PromptScenario
from app.service.prompt_service import prompt_service


logger = get_logger(__name__)


async def chat_with_ai(
        request: ChatRequest,
        db: AsyncSession,
        redis: Redis | None = None,
        llm_provider: BaseLLMProvider| None = None  
    ) -> ChatResponse:

    latest_user_message = get_latest_user_message(request)
    model = request.model or settings.default_model

    logger.info(
            f"会很开始： model={model} message_count={len(request.messages)}"
        )

    # 缓存
    if redis:
        cached_answer = await get_cached_chat_response(
            redis=redis,
            question=latest_user_message,
        )
        if cached_answer:
            logger.info("对话响应命中缓存")

            return ChatResponse(
                answer=cached_answer,
                model=model,
                session_id=request.session_id,
                message_id=f"m_{uuid.uuid4().hex[:8]}",
                usage=TokenUsage(),
                sources=[],
                trace_id=f"trace_{uuid.uuid4().hex[:8]}",
            )
    llm_provider = llm_provider or LLMProviderFactory.create() # 大模型
    llm_request = build_llm_request_from_chat_request(request) # 请求

    # 调用大模型
    try:
        llm_response = await llm_provider.chat(llm_request)
    except LLMProviderError as exc:
        logger.exception(
            f"chat_llm_provider_error provider={exc.provider} "
            f"status_code={exc.status_code}"
        )
        raise AppException(
            message=exc.message,
            code=ErrorCode.LLM_CALL_FAILED,
            status_code=500,
            data={
                "provider": exc.provider,
                "status_code": exc.status_code,
            },
        ) from exc
    
    answer = llm_response.content


    usage = TokenUsage(
        prompt_tokens=llm_response.usage.prompt_tokens,
        completion_tokens=llm_response.usage.completion_tokens,
        total_tokens=llm_response.usage.total_tokens,
    )
   

    sources = build_mock_sources(latest_user_message)
    await conversation_repository.add_message(
        db=db,
        conversation_id=request.session_id,
        role=MessageRole.ASSISTANT.value,
        content=answer,
        model=model,
        prompt_tokens=usage.prompt_tokens,
        completion_tokens=usage.completion_tokens,
        total_tokens=usage.total_tokens,
    )
    # 缓存答案
    if redis:
        await cache_chat_response(
            redis=redis,
            question=latest_user_message,
            answer=answer,
        )
    # 消息存储数据库    
    if db and request.session_id:
        await conversation_repository.add_message(
            db=db,
            conversation_id=request.session_id,
            role=MessageRole.USER.value,
            content=latest_user_message,
            model=model,
            prompt_tokens=usage.prompt_tokens,
        )
    # 存回答
        await conversation_repository.add_message(
            db=db,
            conversation_id=request.session_id,
            role=MessageRole.ASSISTANT.value,
            content=answer,
            model=model,
            prompt_tokens=usage.prompt_tokens,
            completion_tokens=usage.completion_tokens,
            total_tokens=usage.total_tokens,
        )    
    logger.info(
        f"回答成功：model={model} answer_length={len(answer)} "
        f"total_tokens={usage.total_tokens}"
    )
    return ChatResponse(
        answer = answer,
        model= model,
        session_id=request.session_id,
        message_id=f"m_{uuid.uuid4().hex[:8]}",
        usage=usage,
        sources=sources,
        trace_id=f"trace_{uuid.uuid4().hex[:8]}",
    )


def build_prompt_messages_for_chat(request: ChatRequest) -> list[LLMMessage]:
    has_system_message = any(
        message.role == MessageRole.SYSTEM
        for message in request.messages
    )
    if has_system_message:
        return [
            LLMMessage(
                role=LLMRole(message.role.value),
                content=message.content,
            )
            for message in request.messages
        ]
    latest_user_message = get_latest_user_message(request)
    # 电商场景
    if request.prompt_scenario == PromptScenario.ECOMMERCE_CUSTOMER_SERVICE.value:
        version = request.prompt_version or "v1"
        return prompt_service.render_by_scenario(
            scenario=PromptScenario.ECOMMERCE_CUSTOMER_SERVICE,
            version=version,
            variables={
                "user_question": latest_user_message,
                "business_rules": request.metadata.get(
                    "business_rules",
                    "暂无额外业务规则。",
                ),
                "order_info": request.metadata.get(
                    "order_info",
                    "用户未提供订单信息。",
                ),
            },
        )

    return prompt_service.render_by_scenario(
        scenario=PromptScenario.GENERAL_CHAT,
        variables={
            "user_question": latest_user_message,
        },
    )

def build_llm_request_from_chat_request(request: ChatRequest) -> LLMRequest:
    return LLMRequest(
        model=request.model,
        messages=build_prompt_messages_for_chat(request), # 增加提示词模板
        temperature=request.temperature,
        stream=request.stream,
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

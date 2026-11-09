import uuid

from app.schema.chat import SourceDocument, TokenUsage
from app.schema.rag import RAGQueryRequest, RAGQueryResponse
from app.repositories.knowledge_repository import knowledge_repository

async def query_rag(request: RAGQueryRequest) -> RAGQueryResponse:
    sources = await knowledge_repository.search_documents(
        question=request.question,
        knowledge_base_id=request.knowledge_base_id,
        top_k=request.top_k,
        metadata_filter=request.metadata_filter,
    )
    answer = f"根据知识库 {request.knowledge_base_id} 的内容，RAG 是检索增强生成。"
    return RAGQueryResponse(
        answer=answer,
        knowledge_base_id=request.knowledge_base_id,
        sources=sources,
        usage=TokenUsage(
            prompt_tokens=len(request.question),
            completion_tokens=len(answer),
            total_tokens=len(request.question) + len(answer),
        ),
        trace_id=f"trace_{uuid.uuid4().hex[:8]}",
    )
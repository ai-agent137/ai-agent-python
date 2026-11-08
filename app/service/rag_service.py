import uuid

from app.schema.chat import SourceDocument, TokenUsage
from app.schema.rag import RAGQueryRequest, RAGQueryResponse


async def query_rag(request: RAGQueryRequest) -> RAGQueryResponse:
    source = SourceDocument(
        document_id="doc_001",
        title="AI Agent 课程资料",
        content="RAG 是检索增强生成，用于让大模型结合外部知识回答问题。",
        score=0.92,
        metadata={
            "knowledge_base_id": request.knowledge_base_id,
            "page": 1,
        },
    )

    answer = f"根据知识库 {request.knowledge_base_id} 的内容，RAG 是检索增强生成。"

    return RAGQueryResponse(
        answer=answer,
        knowledge_base_id=request.knowledge_base_id,
        sources=[source],
        usage=TokenUsage(
            prompt_tokens=len(request.question),
            completion_tokens=len(answer),
            total_tokens=len(request.question) + len(answer),
        ),
        trace_id=f"trace_{uuid.uuid4().hex[:8]}",
    )
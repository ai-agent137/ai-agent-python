from fastapi import APIRouter

from app.schema.rag import RAGQueryRequest, RAGQueryResponse
from app.schema.response import Response
from app.service.rag_service import query_rag

router = APIRouter()


@router.post("/rag/query", response_model=Response[RAGQueryResponse])
async def rag_query(
    request: RAGQueryRequest,
) -> Response[RAGQueryResponse]:
    result = await query_rag(request)

    return Response[RAGQueryResponse](
        data=result
    )
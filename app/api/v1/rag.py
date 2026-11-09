from fastapi import APIRouter
import uuid
from app.schema.rag import RAGQueryRequest, RAGQueryResponse
from app.schema.response import ApiResponse
from app.service.rag_service import query_rag

router = APIRouter()


@router.post("/rag/query", response_model=ApiResponse[RAGQueryResponse])
async def rag_query(
    request: RAGQueryRequest,
) -> ApiResponse[RAGQueryResponse]:
    answer = await query_rag(request=request)

    return ApiResponse[RAGQueryResponse](
        data=answer
    )
    
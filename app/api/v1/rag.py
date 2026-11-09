from fastapi import APIRouter
import uuid
from app.schema.rag import RAGQueryRequest, RAGQueryResponse
from app.schema.response import Response
from app.service.rag_service import query_rag

router = APIRouter()


@router.post("/rag/query", response_model=Response[RAGQueryResponse])
async def rag_query(
    request: RAGQueryRequest,
) -> Response[RAGQueryResponse]:
    answer = await query_rag(request=request)

    return Response[RAGQueryResponse](
        data=answer
    )
    
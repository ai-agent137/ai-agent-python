from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from app.dependencies.agent_context import AgentContext, get_agent_context
from app.schema.response import Response

router = APIRouter()


class AgentRunRequest(BaseModel):
    question: str = Field(..., min_length=1, description="用户问题")
    agent_id: str = Field(default="agent_chat", description="Agent ID")


class AgentRunResponse(BaseModel):
    answer: str = Field(..., description="Agent 回答")
    trace_id: str = Field(..., description="链路追踪 ID")
    debug: bool = Field(default=False, description="是否调试模式")


@router.post("/agents/run", response_model=Response[AgentRunResponse])
async def run_agent(
    request: AgentRunRequest,
    context: AgentContext = Depends(get_agent_context),
) -> Response[AgentRunResponse]:
    answer = (
        f"用户 {context.current_user.username} 调用了 {request.agent_id}，"
        f"问题是：{request.question}"
    )

    return Response[AgentRunResponse](
        data=AgentRunResponse(
            answer=answer,
            trace_id=context.trace_id,
            debug=context.debug,
        )
    )
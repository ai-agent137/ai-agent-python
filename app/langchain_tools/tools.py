import json

from langchain_core.tools import StructuredTool, tool

from app.langchain_tools.ecommerce_functions import (
    query_logistics,
    query_order,
    transfer_human,
)
from app.langchain_tools.schemas import (
    QueryLogisticsArgs,
    QueryOrderArgs,
    TransferHumanArgs,
)


@tool
async def query_order_simple(order_id: str) -> str:
    """根据订单号查询订单状态和物流信息。当用户询问订单状态、发货状态、物流状态时使用。"""
    result = await query_order(order_id=order_id)

    return json.dumps(
        result.model_dump(),
        ensure_ascii=False,
    )


@tool
async def query_logistics_simple(tracking_no: str) -> str:
    """根据物流单号查询物流轨迹。当用户已经提供物流单号，并询问包裹运输状态时使用。"""
    result = await query_logistics(tracking_no=tracking_no)

    return json.dumps(
        result.model_dump(),
        ensure_ascii=False,
    )


@tool
async def transfer_human_simple(reason: str) -> str:
    """当用户明确要求人工客服，或者问题超出 AI 能力范围时创建人工客服工单。"""
    result = await transfer_human(reason=reason)

    return json.dumps(
        result.model_dump(),
        ensure_ascii=False,
    )



query_order_tool = StructuredTool.from_function(
    coroutine=query_order,
    name="query_order",
    description=(
        "根据订单号查询订单状态和物流信息。"
        "当用户询问订单状态、发货状态、物流状态时使用。"
        "如果用户没有提供订单号，不要调用该工具，应先追问订单号。"
    ),
    args_schema=QueryOrderArgs,
)


query_logistics_tool = StructuredTool.from_function(
    coroutine=query_logistics,
    name="query_logistics",
    description=(
        "根据物流单号查询物流轨迹。"
        "当用户已经提供物流单号，并询问包裹运输状态时使用。"
    ),
    args_schema=QueryLogisticsArgs,
)


transfer_human_tool = StructuredTool.from_function(
    coroutine=transfer_human,
    name="transfer_human",
    description=(
        "当用户明确要求人工客服，或者问题超出 AI 能力范围时创建人工客服工单。"
        "该工具只创建工单，不处理退款、赔付、删除、支付等高风险操作。"
    ),
    args_schema=TransferHumanArgs,
)


ECOMMERCE_LANGCHAIN_TOOLS = [
    query_order_tool,
    query_logistics_tool,
    transfer_human_tool,
]
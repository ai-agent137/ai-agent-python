import operator
from typing import Annotated, Literal, TypedDict

from langchain_core.messages import AnyMessage, HumanMessage
from langgraph.graph.message import add_messages


class RefundOrderInfo(TypedDict, total=False):
    order_id: str
    status: str
    status_text: str
    amount: float
    currency: str


class HumanDecision(TypedDict, total=False):
    type: Literal["approve", "reject", "edit"]
    reviewer_id: str
    reason: str | None
    edited_payload: dict | None


class HITLState(TypedDict):
    user_question: str
    messages: Annotated[list[AnyMessage], add_messages]

    intent: Literal[
        "general",
        "refund",
        "query_order",
        "human_service",
        "unknown",
    ]

    order_id: str | None
    order_info: RefundOrderInfo | None

    refund_amount: float | None
    refund_reason: str | None

    risk_level: Literal["low", "medium", "high"]
    need_human_confirm: bool
    pending_action: str | None
    pending_payload: dict | None

    human_decision: HumanDecision | None
    action_result: dict | None

    final_answer: str
    is_finished: bool

    logs: Annotated[list[str], operator.add]
    errors: Annotated[list[str], operator.add]

def create_initial_state(
    user_question: str,
) -> HITLState:
    return {
        "user_question": user_question,
        "messages": [
            HumanMessage(content=user_question)
        ],

        "intent": "unknown",

        "order_id": None,
        "order_info": None,

        "refund_amount": None,
        "refund_reason": None,

        "risk_level": "low",
        "need_human_confirm": False,
        "pending_action": None,
        "pending_payload": None,

        "human_decision": None,
        "action_result": None,

        "final_answer": "",
        "is_finished": False,

        "logs": [],
        "errors": [],
    }    
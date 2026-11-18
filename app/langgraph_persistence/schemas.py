import operator
from typing import Annotated, Literal, TypedDict
from langchain_core.messages import AnyMessage, HumanMessage
from langgraph.graph.message import add_messages

class PersistenceState(TypedDict):
    user_question: str
    messages: Annotated[list[AnyMessage], add_messages]
    intent: Literal[
        "general",
        "refund",
        "query_order",
        "human_service",
        "unknow"
    ]
    order_id: str | None
    order_status: str | None
    policy_answer: str | None
    need_user_input: bool
    waiting_for: str | None
    final_answer: str
    is_finished: bool
    logs: Annotated[list[str], operator.add]
    errors: Annotated[list[str], operator.add]

def create_initial_state(
    user_question: str
) -> PersistenceState:
     return {
        "user_question": user_question,
        "messages": [
            HumanMessage(content=user_question)
        ],

        "intent": "unknown",

        "order_id": None,
        "order_status": None,
        "policy_answer": None,

        "need_user_input": False,
        "waiting_for": None,

        "final_answer": "",
        "is_finished": False,

        "logs": [],
        "errors": [],
    }
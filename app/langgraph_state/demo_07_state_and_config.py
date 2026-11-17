from typing import TypedDict

from langchain_core.runnables import RunnableConfig
from langgraph.graph import END, START, StateGraph


class OrderState(TypedDict):
    user_question: str
    order_id: str | None
    answer: str


def extract_order_id_node(state: OrderState) -> dict:
    question = state["user_question"]

    if "10001" in question:
        return {"order_id": "10001"}

    return {"order_id": None}


def query_order_node(
    state: OrderState,
    config: RunnableConfig,
) -> dict:
    user_id = config.get("configurable", {}).get("user_id", "unknown")

    if not state["order_id"]:
        return {
            "answer": "请提供订单号。"
        }

    return {
        "answer": (
            f"用户 {user_id} 正在查询订单 {state['order_id']}。"
            "这里应该继续做订单归属校验。"
        )
    }


def build_graph():
    graph = StateGraph(OrderState)

    graph.add_node("extract_order_id", extract_order_id_node)
    graph.add_node("query_order", query_order_node)

    graph.add_edge(START, "extract_order_id")
    graph.add_edge("extract_order_id", "query_order")
    graph.add_edge("query_order", END)

    return graph.compile()


def main():
    app = build_graph()

    result = app.invoke(
        {
            "user_question": "帮我查一下订单 10001。",
            "order_id": None,
            "answer": "",
        },
        config={
            "configurable": {
                "thread_id": "thread_order_001",
                "user_id": "u_10001",
                "tenant_id": "tenant_001",
            }
        },
    )

    print(result)


if __name__ == "__main__":
    main()
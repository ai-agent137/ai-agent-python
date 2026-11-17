from typing import TypedDict

from langgraph.graph import END, START, StateGraph


class InputState(TypedDict):
    question: str


class OverallState(TypedDict):
    question: str
    intent: str
    answer: str
    debug_info: str


class OutputState(TypedDict):
    answer: str


def classify_node(state: OverallState) -> dict:
    question = state["question"]

    if "退款" in question:
        intent = "refund"
    else:
        intent = "general"

    return {
        "intent": intent,
        "debug_info": f"识别意图为 {intent}",
    }


def answer_node(state: OverallState) -> dict:
    return {
        "answer": f"当前意图是 {state['intent']}，问题是：{state['question']}"
    }


def build_graph():
    graph = StateGraph(
        OverallState,
        input_schema=InputState,
        output_schema=OutputState,
    )

    graph.add_node("classify", classify_node)
    graph.add_node("answer", answer_node)

    graph.add_edge(START, "classify")
    graph.add_edge("classify", "answer")
    graph.add_edge("answer", END)

    return graph.compile()


def main():
    app = build_graph()

    result = app.invoke({
        "question": "我的订单可以退款吗？"
    })

    print(result)


if __name__ == "__main__":
    main()
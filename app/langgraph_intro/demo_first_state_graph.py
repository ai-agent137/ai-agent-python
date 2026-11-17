from typing import TypedDict

from langgraph.graph import END, START, StateGraph


class SimpleState(TypedDict):
    user_question: str
    answer: str


def answer_node(state: SimpleState) -> dict:
    question = state["user_question"]

    return {
        "answer": f"你问的是：{question}。这是 LangGraph 的第一个节点回答。"
    }


def build_graph():
    graph = StateGraph(SimpleState)

    graph.add_node("answer", answer_node)

    graph.add_edge(START, "answer")
    graph.add_edge("answer", END)

    return graph.compile()


def main():
    app = build_graph()

    result = app.invoke({
        "user_question": "为什么需要 LangGraph？",
        "answer": "",
    })

    print(result)


if __name__ == "__main__":
    main()
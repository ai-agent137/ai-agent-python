from typing import TypedDict

from langgraph.graph import END, START, StateGraph


class QAState(TypedDict):
    user_question: str
    answer: str


def answer_node(state: QAState) -> dict:
    question = state["user_question"]

    return {
        "answer": f"你问的是：{question}。这是 TypedDict State 示例。"
    }


def build_graph():
    graph = StateGraph(QAState)

    graph.add_node("answer", answer_node)

    graph.add_edge(START, "answer")
    graph.add_edge("answer", END)

    return graph.compile()


def main():
    app = build_graph()

    result = app.invoke({
        "user_question": "TypedDict State 有什么用？",
        "answer": "",
    })

    print(result)


if __name__ == "__main__":
    main()
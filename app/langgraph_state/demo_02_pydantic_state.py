from pydantic import BaseModel, Field

from langgraph.graph import END, START, StateGraph


class PydanticQAState(BaseModel):
    user_question: str = Field(..., min_length=1, description="用户问题")
    answer: str = Field(default="", description="最终回答")


def answer_node(state: PydanticQAState) -> dict:
    return {
        "answer": f"你问的是：{state.user_question}。这是 Pydantic State 示例。"
    }


def build_graph():
    graph = StateGraph(PydanticQAState)

    graph.add_node("answer", answer_node)

    graph.add_edge(START, "answer")
    graph.add_edge("answer", END)

    return graph.compile()


def main():
    app = build_graph()

    result = app.invoke({
        "user_question": "Pydantic State 适合什么场景？",
    })

    print(result)


if __name__ == "__main__":
    main()
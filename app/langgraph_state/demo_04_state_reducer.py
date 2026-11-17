from typing import Annotated, TypedDict

from langgraph.graph import END, START, StateGraph


def merge_unique_list(
    old: list[str],
    new: list[str],
) -> list[str]:
    result = list(old)

    for item in new:
        if item not in result:
            result.append(item)

    return result


class SourceState(TypedDict):
    question: str
    sources: Annotated[list[str], merge_unique_list]
    answer: str


def retrieve_employee_doc_node(state: SourceState) -> dict:
    return {
        "sources": ["employee_handbook"]
    }


def retrieve_policy_doc_node(state: SourceState) -> dict:
    return {
        "sources": ["ecommerce_after_sales", "employee_handbook"]
    }


def answer_node(state: SourceState) -> dict:
    return {
        "answer": f"最终引用来源：{', '.join(state['sources'])}"
    }


def build_graph():
    graph = StateGraph(SourceState)

    graph.add_node("retrieve_employee_doc", retrieve_employee_doc_node)
    graph.add_node("retrieve_policy_doc", retrieve_policy_doc_node)
    graph.add_node("answer", answer_node)

    graph.add_edge(START, "retrieve_employee_doc")
    graph.add_edge("retrieve_employee_doc", "retrieve_policy_doc")
    graph.add_edge("retrieve_policy_doc", "answer")
    graph.add_edge("answer", END)

    return graph.compile()


def main():
    app = build_graph()

    result = app.invoke({
        "question": "员工售后规则是什么？",
        "sources": [],
        "answer": "",
    })

    print(result)


if __name__ == "__main__":
    main()
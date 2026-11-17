from langchain_core.messages import AIMessage, HumanMessage
from langgraph.graph import END, START, MessagesState, StateGraph


def assistant_node(state: MessagesState) -> dict:
    last_message = state["messages"][-1]

    return {
        "messages": [
            AIMessage(
                content=f"我收到你的消息了：{last_message.content}"
            )
        ]
    }


def build_graph():
    graph = StateGraph(MessagesState)

    graph.add_node("assistant", assistant_node)

    graph.add_edge(START, "assistant")
    graph.add_edge("assistant", END)

    return graph.compile()


def main():
    app = build_graph()

    result = app.invoke({
        "messages": [
            HumanMessage(content="MessagesState 有什么用？")
        ]
    })

    for message in result["messages"]:
        print(message.type, ":", message.content)


if __name__ == "__main__":
    main()
from langchain_core.messages import HumanMessage, SystemMessage

from app.langchain_models.model_factory import LangChainModelFactory


def main():
    model = LangChainModelFactory.create(
        provider="qwen",
        model="deepseek-v4.1-flash-1017",
        temperature=0.7,
    )

    messages = [
        SystemMessage(content="你是一个专业 AI Agent 课程助教。"),
        HumanMessage(content="请用三句话解释 LangChain ChatModel。"),
    ]

    response = model.invoke(messages)

    print("response class:", response.__class__.__name__)
    print("message type:", response.type)
    print("content:")
    print(response.content)
    print("response_metadata:")
    print(response.response_metadata)
    print("usage_metadata:")
    print(response.usage_metadata)


if __name__ == "__main__":
    main()
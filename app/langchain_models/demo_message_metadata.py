from langchain_core.messages import HumanMessage, SystemMessage

from app.langchain_models.model_factory import LangChainModelFactory


def main():
    model = LangChainModelFactory.create(
        provider="qwen",
        model="deepseek-v4.1-flash-1017",
        temperature=0.7,
    )

    response = model.invoke([
        SystemMessage(content="你是一个专业 AI Agent 课程助教。"),
        HumanMessage(content="请用一句话解释 response_metadata。"),
    ])

    print("content:")
    print(response.content)
    print("=" * 80)

    print("response_metadata:")
    print(response.response_metadata)
    print("=" * 80)

    print("usage_metadata:")
    print(response.usage_metadata)
    print("=" * 80)

    print("id:")
    print(response.id)


if __name__ == "__main__":
    main()
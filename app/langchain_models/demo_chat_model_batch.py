from app.langchain_models.model_factory import LangChainModelFactory


def main():
    model = LangChainModelFactory.create(
        provider="qwen",
        model="deepseek-v4.1-flash-1017",
        temperature=0.7,
    )

    questions = [
        "什么是 LangChain？",
        "什么是 LangGraph？",
        "什么是 RAG？",
    ]

    responses = model.batch(questions)

    for question, response in zip(questions, responses):
        print("question:", question)
        print("answer:", response.content)
        print("=" * 80)


if __name__ == "__main__":
    main()
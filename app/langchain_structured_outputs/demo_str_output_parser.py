from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from app.langchain_models.model_factory import LangChainModelFactory


def main():
    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            "你是一个专业 AI Agent 课程助教。",
        ),
        (
            "human",
            "请用三句话解释：{topic}",
        ),
    ])

    model = LangChainModelFactory.create(
        provider="qwen",
        model="deepseek-v4.1-flash-1017",
        temperature=0.7,
    )

    parser = StrOutputParser()

    chain = prompt | model | parser

    result = chain.invoke({
        "topic": "StrOutputParser 的作用",
    })

    print("result type:", type(result))
    print("result:")
    print(result)


if __name__ == "__main__":
    main()
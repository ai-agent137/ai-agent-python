from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain_openai import ChatOpenAI

from app.core.config import settings


def create_model() -> ChatOpenAI:
    if not settings.dashscope_api_key:
            raise RuntimeError("请先在 .env 中配置 DASHSCOPE_API_KEY")
    
    return ChatOpenAI(
            model="deepseek-v4.1-flash-1017",
            api_key=settings.dashscope_api_key,
            base_url=settings.qwen_base_url,
            temperature=0.7,
    )


def add_prefix(text: str) -> str:
    return f"【LangChain 架构解释】\n{text}"


def main():
    prompt = ChatPromptTemplate.from_messages([
        ("system", "你是一个专业 AI Agent 课程助教。"),
        ("human", "请用三句话解释：{topic}"),
    ])

    model = create_model()
    parser = StrOutputParser()
    prefix = RunnableLambda(add_prefix)

    chain = prompt | model | parser | prefix

    result = chain.invoke({
        "topic": "Runnable 为什么是 LangChain 的核心",
    })

    print(result)


if __name__ == "__main__":
    main()
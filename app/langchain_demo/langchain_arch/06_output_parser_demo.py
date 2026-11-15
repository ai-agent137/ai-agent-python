from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from app.core.config import settings


def create_chat_model() -> ChatOpenAI:
    if not settings.dashscope_api_key:
            raise RuntimeError("请先在 .env 中配置 DASHSCOPE_API_KEY")
    
    return ChatOpenAI(
            model="deepseek-v4.1-flash-1017",
            api_key=settings.dashscope_api_key,
            base_url=settings.qwen_base_url,
            temperature=0.7,
    )


def main():
    prompt = ChatPromptTemplate.from_messages([
        ("system", "你是一个专业 AI Agent 课程助教。"),
        ("human", "请用一句话解释：{topic}"),
    ])

    model = create_chat_model()

    chain = prompt | model | StrOutputParser()

    result = chain.invoke({
        "topic": "LangChain OutputParser",
    })

    print("result type:", type(result))
    print("result:", result)


if __name__ == "__main__":
    main()
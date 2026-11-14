from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from app.core.config import settings


def create_model():
    return ChatOpenAI(
        model="deepseek-v4.1-flash-1017",
        api_key=settings.dashscope_api_key,
        base_url=settings.qwen_base_url,
        temperature=0.7,
    )


def run_simple_chain():
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

    model = create_model()

    chain = prompt | model

    response = chain.invoke({
        "topic": "LangChain 的价值",
    })

    print(response.content)


if __name__ == "__main__":
    run_simple_chain()
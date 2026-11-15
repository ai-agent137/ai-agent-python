from langchain_core.messages import HumanMessage, SystemMessage
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
    model = create_chat_model()

    messages = [
        SystemMessage(content="你是一个专业 AI Agent 课程助教。"),
        HumanMessage(content="请用一句话解释 LangChain ChatModel。"),
    ]

    response = model.invoke(messages)

    print("response type:", type(response))
    print("response message type:", response.type)
    print("content:")
    print(response.content)
    print("metadata:")
    print(response.response_metadata)


if __name__ == "__main__":
    main()
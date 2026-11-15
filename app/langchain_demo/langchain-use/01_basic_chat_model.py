
from urllib import response

from langchain.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_openai import ChatOpenAI
from pydantic.v1 import create_model

from app.core.config import settings

def create_chat_model():
    if not settings.dashscope_api_key:
        raise RuntimeError("请先在 .env 中配置 DASHSCOPE_API_KEY")

    return ChatOpenAI(
        model="deepseek-v4.1-flash-1017",
        api_key=settings.dashscope_api_key,
        base_url=settings.qwen_base_url,
        temperature=0.7,
    )



def run_basic_chat():
    # 创建一个简单的聊天模型
    model = create_chat_model()
    response = model.invoke("Hello! How are you today?")
    print(response)
def chat_with_messages():
    model = create_chat_model()
    messages = [
        SystemMessage(content="You are a helpful assistant! Your name is Bob."),
        HumanMessage(content="What is your name?"),
    ]
    response = model.invoke(messages)
    print(SystemMessage(content="You are a helpful assistant! Your name is Bob."))    


def run_prompt_template():

    # 创建一个简单的提示模板
    prompt = ChatPromptTemplate.from_messages([
        ("system", "你是一个专业的 {role_name}，回答要简洁、准确。"),
        ("human", "请解释一下：{question}"),
    ])

    # 使用模板生成提示
    result = prompt.invoke({
        "role_name": "AI Agent 课程助教",
        "question": "为什么需要 LangChain？",
    })

    print("prompt result type:", type(result))
    print("messages:")
    for message in result.messages:
        print(message.type, ":", message.content)
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
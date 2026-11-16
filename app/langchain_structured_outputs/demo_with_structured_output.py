from app.langchain_models.model_factory import LangChainModelFactory
from app.schema.prompt import IntentClassificationResult
from langchain_core.messages import SystemMessage, HumanMessage

def main():
    model=LangChainModelFactory.create(
        provider="qwen",
        model="deepseek-v4.1-flash-1017",
        temperature=0.7
    )

    structured_model = model.with_structured_output(
        IntentClassificationResult
    )
    result = structured_model.invoke([
        SystemMessage(
            content=(
                "你是一个电商客服意图识别器。\n"
                "请根据用户问题输出结构化分类结果。"
            )
        ),
        HumanMessage(
            content="我的订单怎么还没发货？"
        ),
    ])

    print("result type:", type(result))
    print(result.model_dump())

if __name__ == "__main__":
    main()
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.tools import tool

from app.langchain_models.model_factory import LangChainModelFactory


@tool
def query_order(order_id: str) -> str:
    """根据订单号查询订单状态和物流信息。"""
    if order_id == "10001":
        return "订单 10001 已发货，物流公司顺丰，物流单号 SF10001。"

    return f"未查询到订单 {order_id}。"


def main():
    model = LangChainModelFactory.create(
        provider="qwen",
        model="deepseek-v4.1-flash-1017",
        temperature=0.7,
    )

    model_with_tools = model.bind_tools([query_order])

    messages = [
        SystemMessage(
            content=(
                "你是一个电商客服助手。\n"
                "当用户询问订单状态时，优先调用工具查询真实信息。"
            )
        ),
        HumanMessage(content="帮我查一下订单 10001 到哪了？"),
    ]

    response = model_with_tools.invoke(messages)

    print("content:")
    print(response.content)
    print("=" * 80)

    print("tool_calls:")
    print(response.tool_calls)
    print("=" * 80)

    if response.tool_calls:
        first_tool_call = response.tool_calls[0]
        print("tool name:", first_tool_call["name"])
        print("tool args:", first_tool_call["args"])
        print("tool id:", first_tool_call["id"])


if __name__ == "__main__":
    main()
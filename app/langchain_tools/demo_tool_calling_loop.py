import asyncio

from langchain_core.messages import HumanMessage, SystemMessage

from app.langchain_models.model_factory import LangChainModelFactory
from app.langchain_tools.executor import langchain_tool_executor
from app.langchain_tools.registry import langchain_tool_registry


async def main():
    model = LangChainModelFactory.create(
        provider="qwen",
        model="deepseek-v4.1-flash-1017",
        temperature=0,
    )

    tools = langchain_tool_registry.get_many([
        "query_order",
        "query_logistics",
        "transfer_human",
    ])

    model_with_tools = model.bind_tools(tools)

    messages = [
        SystemMessage(
            content=(
                "你是一个跨境电商客服助手。\n"
                "当用户询问订单、物流、发货状态时，必须优先调用工具查询真实信息。\n"
                "工具返回结果后，请用礼貌、简洁的中文回复用户。\n"
                "不要编造订单状态、物流公司或物流单号。"
            )
        ),
        HumanMessage(
            content="帮我查一下订单 10001 到哪了？"
        ),
    ]

    first_response = await model_with_tools.ainvoke(messages)

    print("first_response content:")
    print(first_response.content)
    print("=" * 80)

    print("tool_calls:")
    print(first_response.tool_calls)
    print("=" * 80)

    if not first_response.tool_calls:
        print("模型没有请求工具，直接回答：")
        print(first_response.content)
        return

    tool_messages = await langchain_tool_executor.execute_tool_calls(
        first_response.tool_calls
    )

    messages.append(first_response)
    messages.extend(tool_messages)

    final_response = await model.ainvoke(messages)

    print("final answer:")
    print(final_response.content)


if __name__ == "__main__":
    asyncio.run(main())
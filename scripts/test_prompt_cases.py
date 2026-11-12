from app.prompts.base import PromptScenario
from app.service.prompt_service import prompt_service


TEST_CASES = [
    {
        "name": "未提供订单号",
        "question": "我的订单怎么还没发货？",
        "order_info": "用户未提供订单号。",
    },
    {
        "name": "提供订单号",
        "question": "订单 10001 到哪了？",
        "order_info": "订单 10001，状态：已发货，物流公司：顺丰，物流单号：SF10001。",
    },
    {
        "name": "要求编造物流",
        "question": "你帮我编一个物流单号吧。",
        "order_info": "无订单信息。",
    },
]


def main():
    for case in TEST_CASES:
        print("测试用例：", case["name"])

        messages = prompt_service.render_by_scenario(
            scenario=PromptScenario.ECOMMERCE_CUSTOMER_SERVICE,
            version="v2",
            variables={
                "user_question": case["question"],
                "business_rules": "没有订单号不能查询具体物流；不能编造物流信息。",
                "order_info": case["order_info"],
            },
        )

        for message in messages:
            print("role:", message.role.value)
            print(message.content[:500])
            print()

        print("=" * 80)


if __name__ == "__main__":
    main()
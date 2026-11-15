from langchain_core.tools import tool


@tool
def query_order(order_id: str) -> str:
    """根据订单号查询订单状态和物流信息。"""
    if order_id == "10001":
        return "订单 10001 已发货，物流公司顺丰，物流单号 SF10001。"

    return f"未查询到订单 {order_id}。"
def run_tool():
    print(query_order.name)
    print(query_order.description)
    print(query_order.args)
    result = query_order.invoke("10001")
    print(result)


if __name__ == "__main__":
    run_tool()
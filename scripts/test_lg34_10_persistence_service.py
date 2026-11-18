from app.langgraph_persistence.service import langgraph_persistence_service


def main():
    tenant_id = "tenant_001"
    user_id = "u_10001"
    conversation_id = "conv_refund_001"

    first = langgraph_persistence_service.start_refund_flow(
        user_question="我要退款。",
        tenant_id=tenant_id,
        user_id=user_id,
        conversation_id=conversation_id,
    )

    print("first:")
    print("final_answer:", first["final_answer"])
    print("intent:", first["intent"])
    print("waiting_for:", first["waiting_for"])
    print("=" * 80)

    second = langgraph_persistence_service.continue_flow(
        user_question="订单号是 10002。",
        tenant_id=tenant_id,
        user_id=user_id,
        conversation_id=conversation_id,
    )

    print("second:")
    print("final_answer:", second["final_answer"])
    print("intent:", second["intent"])
    print("order_id:", second["order_id"])
    print("order_status:", second["order_status"])
    print("=" * 80)

    current = langgraph_persistence_service.get_current_state(
        tenant_id=tenant_id,
        user_id=user_id,
        conversation_id=conversation_id,
    )

    print("current state:")
    print(current["values"])


if __name__ == "__main__":
    main()
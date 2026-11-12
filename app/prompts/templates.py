from app.prompts.base import (
    PromptMessageTemplate,
    PromptRole,
    PromptScenario,
    PromptTemplate,
)


GENERAL_CHAT_PROMPT_V1 = PromptTemplate(
    prompt_id="general_chat",
    name="通用聊天助手",
    scenario=PromptScenario.GENERAL_CHAT,
    version="v1",
    description="用于普通 AI Chat 的基础 Prompt。",
    required_variables=[
        "user_question",
    ],
    messages=[
        PromptMessageTemplate(
            role=PromptRole.SYSTEM,
            template=(
                "你是一个专业、耐心、表达清晰的 AI 助手。\n"
                "回答要求：\n"
                "1. 优先用中文回答。\n"
                "2. 不要编造事实。\n"
                "3. 如果不确定，请明确说明不确定。\n"
                "4. 回答要结构清晰，不要啰嗦。"
            ),
        ),
        PromptMessageTemplate(
            role=PromptRole.USER,
            template="{user_question}",
        ),
    ],
)


INTENT_CLASSIFICATION_PROMPT_V1 = PromptTemplate(
    prompt_id="intent_classification",
    name="用户意图识别 Prompt",
    scenario=PromptScenario.GENERAL_CHAT,
    version="v1",
    description="用于识别用户意图，输出 JSON。",
    required_variables=[
        "user_question",
    ],
    messages=[
        PromptMessageTemplate(
            role=PromptRole.SYSTEM,
            template=(
                "你是一个用户意图识别器。\n"
                "你只能输出 JSON，不要输出任何解释。\n"
                "\n"
                "可选 intent：\n"
                "1. query_order：查询订单\n"
                "2. refund：退款售后\n"
                "3. product_question：商品咨询\n"
                "4. other：其他\n"
                "\n"
                "输出格式：\n"
                "{{\n"
                "  \"intent\": \"query_order | refund | product_question | other\",\n"
                "  \"confidence\": 0.0\n"
                "}}"
            ),
        ),
        PromptMessageTemplate(
            role=PromptRole.USER,
            template="用户问题：{user_question}",
        ),
    ],
)
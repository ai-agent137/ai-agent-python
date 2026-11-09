from app.schema.chat import ChatMessage, MessageRole
from app.schema.conversation import ConversationCreateRequest

class ConversationRespository:
    def __init__(self):
        self._conversations: dict[str, dict] = {}
        self._messages: dict[str, list[ChatMessage]] = {}
    async def create(self, conversation_id: str, request: ConversationCreateRequest) -> dict:
        conversation = {
            "conversation_id": conversation_id,
            "title": request.title,
        }

        self._conversations[conversation_id] = conversation
        self._messages[conversation_id] = []

        return conversation
    async def get_messages(self, conversation_id: str) -> list[ChatMessage]:
        if conversation_id not in self._messages:
            return [
                ChatMessage(
                    role=MessageRole.USER,
                    content="什么是 AI Agent？"
                ),
                ChatMessage(
                    role=MessageRole.ASSISTANT,
                    content="AI Agent 是能够调用工具完成任务的智能体。"
                )
            ]

        return self._messages[conversation_id] 


conversation_respository = ConversationRespository()         
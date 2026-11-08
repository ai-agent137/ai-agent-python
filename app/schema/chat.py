from enum import Enum
from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import List, Any

    
class TokenUsage(BaseModel):
    prompt_tokens: int = Field(default=0, ge=0, description="输入 token 数")
    completion_tokens: int = Field(default=0, ge=0, description="输出 token 数")
    total_tokens: int = Field(default=0, ge=0, description="总 token 数")    


class MessageRole(str, Enum):
    SYSTEM = "system"
    ASSISTANT= "assistant"
    USER = "user"
    TOOL = "tool"
class ChatMessage(BaseModel):
    role: MessageRole = Field(default=..., description="消息角色")
    content: str = Field(..., description="消息内容")


class ChatRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    messages: List[ChatMessage] = Field(default=list, description="聊天消息内容")
    model: str = Field(default="deepseek-chat", description="模型名称")
    temperature: float = Field(default=0.7, ge=0, le=2, description="温度")
    stream: bool = Field(default=False, description="是否开启流式输出")
    session_id: str | None = Field(default=None, description="会话 ID")
    user_id: str | None = Field(default=None, description="用户 ID")
    metadata: dict[str, Any] = Field(default_factory=dict, description="扩展元数据")

    @field_validator("model")
    @classmethod
    def validate_model(cls, value: str) -> str:
        supported_models = ["deepseek-chat", "qwen-plus", "gpt-4o-mini"]

        if value not in supported_models:
            raise ValueError(f"不支持的模型：{value}")

        return value


class ChatResponse(BaseModel):
    answer: str = Field(..., description="AI 回答")
    model: str = Field(..., description="模型名称")
    session_id: str | None = Field(default=None, description="会话 ID")
    message_id: str | None = Field(default=None, description="消息 ID")
    usage: TokenUsage = Field(default_factory=TokenUsage, description="Token 用量")
    sources: list[SourceDocument] = Field(default_factory=list, description="引用来源")
    trace_id: str | None = Field(default=None, description="链路追踪 ID") 




class SourceDocument(BaseModel):
    document_id: str = Field(..., description="文档 ID")
    title: str = Field(..., description="文档标题")
    content: str = Field(..., description="命中的文档片段")
    score: float = Field(default=0.0, ge=0, le=1, description="相关性分数")
    metadata: dict[str, Any] = Field(default_factory=dict, description="文档元数据")    

# title
class GenerateTitleRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=500, description="用户第一条消息")


class GenerateTitleResponse(BaseModel):
    title: str = Field(..., description="生成的会话标题")    
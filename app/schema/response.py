from typing import Any, TypeVar, Generic
from pydantic import BaseModel, Field

T = TypeVar("T")


class Response(BaseModel, Generic[T]):
    code: str = Field(default="200", description="响应码")
    message: str = Field(default="操作成功", description="响应消息")
    data: T | None = Field(default=None, description="响应数据")


class ErrorResponse(BaseModel):
    code: int = Field(default=500, description="错误码")
    message: str = Field(..., description="错误信息")
    detail: str | None = Field(default=None, description="错误详情")
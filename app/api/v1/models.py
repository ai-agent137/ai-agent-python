from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from app.core.config import settings
from app.dependencies.auth import require_admin
from app.schema.response import ApiResponse
from app.schema.user import CurrentUser

router = APIRouter()


class ModelInfo(BaseModel):
    name: str = Field(..., description="模型名称")
    provider: str = Field(default="mock", description="模型厂商")
    support_stream: bool = Field(default=True, description="是否支持流式输出")


class ModelListResponse(BaseModel):
    models: list[ModelInfo] = Field(default_factory=list, description="模型列表")


@router.get("/models", response_model=ApiResponse[ModelListResponse])
async def list_models(  
     admin_user: CurrentUser = Depends(require_admin),
) -> ApiResponse[ModelListResponse]:
    models = [
        ModelInfo(
            name=model,
            provider=get_provider_name(model),
            support_stream=True,
        )
        for model in settings.supported_model_list
    ]

    return ApiResponse[ModelListResponse](
        data=ModelListResponse(models=models)
    )


def get_provider_name(model: str) -> str:
    if model.startswith("deepseek"):
        return "deepseek"

    if model.startswith("qwen"):
        return "qwen"

    if model.startswith("gpt"):
        return "openai"

    return "unknown"
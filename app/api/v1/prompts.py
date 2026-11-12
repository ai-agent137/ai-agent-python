from fastapi import APIRouter

from app.schema.response import ApiResponse
from app.service.prompt_service import prompt_service

router = APIRouter()


@router.get("/prompts", response_model=ApiResponse[list[dict]])
async def list_prompts() -> ApiResponse[list[dict]]:
    prompts = prompt_service.list_prompts()

    return ApiResponse[list[dict]](
        data=[
            {
                "prompt_id": prompt.prompt_id,
                "name": prompt.name,
                "scenario": prompt.scenario.value,
                "version": prompt.version,
                "description": prompt.description,
                "required_variables": prompt.required_variables,
            }
            for prompt in prompts
        ]
    )
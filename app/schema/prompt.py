from typing import Literal

from pydantic import BaseModel, Field


class IntentClassificationResult(BaseModel):
    intent: Literal[
        "query_order",
        "refund",
        "product_question",
        "other",
    ] = Field(..., description="用户意图")

    confidence: float = Field(..., ge=0, le=1, description="置信度")

    
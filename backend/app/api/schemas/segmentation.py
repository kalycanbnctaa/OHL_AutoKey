from typing import Optional
from pydantic import BaseModel, Field

class SegmentRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=5000)

class SegmentResponse(BaseModel):
    text: str
    dp: list[Optional[float]]  
    choices: list[int]
    words: list[str]
    result: str
    cost: float
    success: bool
    error: str | None = None
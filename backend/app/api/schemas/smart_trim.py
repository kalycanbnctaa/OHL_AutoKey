from pydantic import BaseModel, Field

class SmartTrimRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=10000)
    limit: int = Field(..., ge=1, le=5000)

class SmartTrimItemResponse(BaseModel):
    word: str
    weight: int
    value: float

class SmartTrimResponse(BaseModel):
    text: str
    limit: int
    items: list[SmartTrimItemResponse]
    total_value: float
    total_weight: int
    dp_table: list[list[float]]
    success: bool
    error: str | None = None
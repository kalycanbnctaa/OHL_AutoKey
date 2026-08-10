from pydantic import BaseModel, Field

class RecordPairRequest(BaseModel):
    prev: str = Field(..., min_length=1)
    curr: str = Field(..., min_length=1)

class RecordPairResponse(BaseModel):
    success: bool
    total_pairs: int
    unique_pairs: int

class RerankRequest(BaseModel):
    prev: str = Field(..., min_length=1)
    candidates: list[tuple[str, int]] = Field(..., max_length=50)

class RerankItem(BaseModel):
    word: str
    frequency: int
    score: float

class RerankResponse(BaseModel):
    prev: str
    candidates: list[RerankItem]

class StatisticsResponse(BaseModel):
    total_pairs: int
    unique_pairs: int
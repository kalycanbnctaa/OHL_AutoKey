from pydantic import BaseModel, Field


class TrieStatisticsResponse(BaseModel):
    word_count: int = Field(ge=0)
    node_count: int = Field(ge=1)
    average_depth: float = Field(ge=0)
    memory_bytes: int = Field(ge=0)
    memory_megabytes: float = Field(ge=0)
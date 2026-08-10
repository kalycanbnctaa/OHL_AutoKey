from pydantic import BaseModel, Field


class AutocompleteSuggestion(BaseModel):
    word: str
    frequency: int = Field(ge=0)


class AutocompleteResponse(BaseModel):
    prefix: str
    suggestions: list[AutocompleteSuggestion]
    latency_ms: float = Field(ge=0)
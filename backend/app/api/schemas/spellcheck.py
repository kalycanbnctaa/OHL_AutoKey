from pydantic import BaseModel, Field


class SpellCheckCandidateResponse(BaseModel):
    word: str
    distance: int = Field(ge=0)
    frequency: int = Field(ge=0)


class SpellCheckWordResponse(BaseModel):
    word: str
    is_valid: bool
    suggestions: list[SpellCheckCandidateResponse]


class SpellCheckIssueResponse(BaseModel):
    word: str
    start: int = Field(ge=0)
    end: int = Field(ge=0)
    suggestions: list[SpellCheckCandidateResponse]


class SpellCheckTextRequest(BaseModel):
    text: str = Field(default="", max_length=20000)


class SpellCheckTextResponse(BaseModel):
    issues: list[SpellCheckIssueResponse]
    issue_count: int = Field(ge=0)


class LevenshteinTableResponse(BaseModel):
    source: str
    target: str
    table: list[list[int]]
    distance: int = Field(ge=0)
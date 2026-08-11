from fastapi import APIRouter, Body, HTTPException, Query, Request

from app.api.schemas.spellcheck import (
    LevenshteinTableResponse,
    SpellCheckCandidateResponse,
    SpellCheckIssueResponse,
    SpellCheckTextRequest,
    SpellCheckTextResponse,
    SpellCheckWordResponse,
)
from app.core.levenshtein import compute_distance_table
from app.services.spellcheck_service import SpellCheckService

router = APIRouter(tags=["spellcheck"])

def _get_spellcheck_service(request: Request) -> SpellCheckService:
    dictionary_service = getattr(request.app.state, "dictionary_service", None)

    if dictionary_service is None or not dictionary_service.is_loaded:
        raise HTTPException(503, "Dictionary service is not loaded")

    return SpellCheckService(dictionary_service)

@router.get("/spellcheck/word", response_model=SpellCheckWordResponse)
async def check_word(
    request: Request,
    word: str = Query(..., min_length=1, max_length=64),
    max_distance: int = Query(2, ge=0, le=5),
    top_n: int = Query(5, ge=1, le=20),
) -> SpellCheckWordResponse:
    service = _get_spellcheck_service(request)

    is_valid = service.is_valid_word(word)

    suggestions: list[SpellCheckCandidateResponse] = []

    if not is_valid:
        candidates = service.find_words_within_distance(
            word, max_distance=max_distance, limit=top_n
        )

        suggestions = [
            SpellCheckCandidateResponse(
                word=candidate.word,
                distance=candidate.distance,
                frequency=candidate.frequency,
            )
            for candidate in candidates
        ]

    return SpellCheckWordResponse(
        word=word,
        is_valid=is_valid,
        suggestions=suggestions,
    )

@router.post("/spellcheck/check-text", response_model=SpellCheckTextResponse)
async def check_text(
    request: Request,
    payload: SpellCheckTextRequest = Body(...),
    max_distance: int = Query(2, ge=0, le=5),
    top_n: int = Query(5, ge=1, le=20),
) -> SpellCheckTextResponse:
    service = _get_spellcheck_service(request)

    issues = service.check_text(
        payload.text, max_distance=max_distance, top_n=top_n
    )

    return SpellCheckTextResponse(
        issues=[
            SpellCheckIssueResponse(
                word=issue.word,
                start=issue.start,
                end=issue.end,
                suggestions=[
                    SpellCheckCandidateResponse(
                        word=candidate.word,
                        distance=candidate.distance,
                        frequency=candidate.frequency,
                    )
                    for candidate in issue.suggestions
                ],
            )
            for issue in issues
        ],
        issue_count=len(issues),
    )

@router.get("/levenshtein/table", response_model=LevenshteinTableResponse)
async def levenshtein_table(
    source: str = Query(..., max_length=64),
    target: str = Query(..., max_length=64),
) -> LevenshteinTableResponse:
    result = compute_distance_table(source, target)

    return LevenshteinTableResponse(
        source=result.source,
        target=result.target,
        table=result.table,
        distance=result.distance,
    )
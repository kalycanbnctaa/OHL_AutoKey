import time

from fastapi import APIRouter, Query, Request

from app.api.schemas.autocomplete import (
    AutocompleteResponse,
    AutocompleteSuggestion,
)
from app.services.autocomplete_service import AutocompleteService

router = APIRouter(tags=["autocomplete"])


@router.get("/autocomplete", response_model=AutocompleteResponse)
async def autocomplete(
    request: Request,
    prefix: str = Query("", max_length=64),
    top_n: int = Query(5, ge=1, le=20),
) -> AutocompleteResponse:
    dictionary_service = getattr(
        request.app.state, "dictionary_service", None
    )

    if dictionary_service is None or not dictionary_service.is_loaded:
        raise RuntimeError("Dictionary service is not loaded")

    service = AutocompleteService(dictionary_service)

    start = time.perf_counter()
    entries = service.get_suggestions(prefix, top_n)
    elapsed_ms = (time.perf_counter() - start) * 1000

    return AutocompleteResponse(
        prefix=prefix,
        suggestions=[
            AutocompleteSuggestion(word=entry.word, frequency=entry.frequency)
            for entry in entries
        ],
        latency_ms=round(elapsed_ms, 3),
    )
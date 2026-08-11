from fastapi import APIRouter, HTTPException, Request

from app.api.schemas.statistics import TrieStatisticsResponse
from app.utils.statistics import (
    calculate_average_depth,
    estimate_memory_bytes,
    estimate_memory_megabytes,
)

router = APIRouter(tags=["system"])

@router.get(
    "/statistics",
    response_model=TrieStatisticsResponse,
)
async def statistics(request: Request) -> TrieStatisticsResponse:
    dictionary_service = getattr(
        request.app.state,
        "dictionary_service",
        None,
    )

    if dictionary_service is None or not dictionary_service.is_loaded:
        raise HTTPException(503, "Dictionary service is not loaded")

    trie = dictionary_service.trie

    return TrieStatisticsResponse(
        word_count=trie.word_count,
        node_count=trie.node_count,
        average_depth=round(calculate_average_depth(trie), 2),
        memory_bytes=estimate_memory_bytes(trie),
        memory_megabytes=round(estimate_memory_megabytes(trie), 2),
    )
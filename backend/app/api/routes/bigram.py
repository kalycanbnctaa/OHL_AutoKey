from fastapi import APIRouter, Request, HTTPException
from app.api.schemas.bigram import (
    RecordPairRequest,
    RecordPairResponse,
    RerankRequest,
    RerankResponse,
    RerankItem,
    StatisticsResponse,
)
from app.services.bigram_service import BigramService

router = APIRouter(tags=["bigram"])
_bigram_service = BigramService()

@router.post("/bigram/record", response_model=RecordPairResponse)
async def record_pair(request: Request, payload: RecordPairRequest) -> RecordPairResponse:
    session_id = request.headers.get("X-Session-Id")
    if not session_id:
        raise HTTPException(400, "X-Session-Id header required")
    _bigram_service.record_pair(session_id, payload.prev, payload.curr)
    stats = _bigram_service.get_statistics(session_id)
    return RecordPairResponse(
        success=True,
        total_pairs=stats["total_pairs"],
        unique_pairs=stats["unique_pairs"],
    )

@router.post("/bigram/rerank", response_model=RerankResponse)
async def rerank(request: Request, payload: RerankRequest) -> RerankResponse:
    session_id = request.headers.get("X-Session-Id")
    if not session_id:
        raise HTTPException(400, "X-Session-Id header required")
    scored = _bigram_service.rerank_suggestions(session_id, payload.prev, payload.candidates)
    return RerankResponse(
        prev=payload.prev,
        candidates=[
            RerankItem(word=word, frequency=freq, score=score)
            for word, freq, score in scored
        ],
    )

@router.get("/bigram/statistics", response_model=StatisticsResponse)
async def statistics(request: Request) -> StatisticsResponse:
    session_id = request.headers.get("X-Session-Id")
    if not session_id:
        raise HTTPException(400, "X-Session-Id header required")
    stats = _bigram_service.get_statistics(session_id)
    return StatisticsResponse(
        total_pairs=stats["total_pairs"],
        unique_pairs=stats["unique_pairs"],
    )
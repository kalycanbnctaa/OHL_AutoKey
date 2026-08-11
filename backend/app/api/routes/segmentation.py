import math
from fastapi import APIRouter, Request, HTTPException

from app.api.schemas.segmentation import SegmentRequest, SegmentResponse
from app.services.segmentation_service import SegmentationService

router = APIRouter(tags=["segmentation"])

@router.post("/segment", response_model=SegmentResponse)
async def segment(request: Request, payload: SegmentRequest) -> SegmentResponse:
    dictionary_service = getattr(request.app.state, "dictionary_service", None)
    if dictionary_service is None or not dictionary_service.is_loaded:
        raise HTTPException(503, "Dictionary service is not loaded")

    service = SegmentationService(dictionary_service)
    result = service.segment(payload.text)

    if result is None:
        return SegmentResponse(
            text=payload.text,
            dp=[],
            choices=[],
            words=[],
            result="",
            cost=0.0,
            success=False,
            error="Tidak dapat menyegmentasi teks. Pastikan semua kata ada dalam kamus."
        )

    dp_clean = [None if math.isinf(x) else x for x in result.dp]

    return SegmentResponse(
        text=result.text,
        dp=dp_clean,
        choices=result.choices,
        words=result.words,
        result=result.result,
        cost=result.cost,
        success=True,
        error=None,
    )
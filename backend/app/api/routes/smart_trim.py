from fastapi import APIRouter, Request, HTTPException
from app.api.schemas.smart_trim import SmartTrimRequest, SmartTrimResponse, SmartTrimItemResponse
from app.services.smart_trim_service import SmartTrimService

router = APIRouter(tags=["smart_trim"])

@router.post("/smart-trim", response_model=SmartTrimResponse)
async def smart_trim(request: Request, payload: SmartTrimRequest) -> SmartTrimResponse:
    dictionary_service = getattr(request.app.state, "dictionary_service", None)
    if dictionary_service is None or not dictionary_service.is_loaded:
        raise HTTPException(503, "Dictionary service is not loaded")

    service = SmartTrimService(dictionary_service)
    result = service.trim(payload.text, payload.limit)

    if result is None:
        return SmartTrimResponse(
            text=payload.text,
            limit=payload.limit,
            items=[],
            total_value=0.0,
            total_weight=0,
            dp_table=[],
            success=False,
            error="Tidak dapat melakukan trim. Pastikan teks mengandung kata-kata yang valid dalam kamus."
        )

    return SmartTrimResponse(
        text=payload.text,
        limit=payload.limit,
        items=[
            SmartTrimItemResponse(
                word=word,
                weight=weight,
                value=value
            )
            for word, weight, value in result.items
        ],
        total_value=result.total_value,
        total_weight=result.total_weight,
        dp_table=result.dp_table,
        success=True,
        error=None,
    )
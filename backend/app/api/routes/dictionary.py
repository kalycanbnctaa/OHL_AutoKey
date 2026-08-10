from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, Field

router = APIRouter(tags=["dictionary"])

class AddWordRequest(BaseModel):
    word: str = Field(..., min_length=1, max_length=64)

@router.post("/dictionary/add")
async def add_word(request: Request, payload: AddWordRequest) -> dict:
    dictionary_service = getattr(request.app.state, "dictionary_service", None)
    if dictionary_service is None or not dictionary_service.is_loaded:
        raise RuntimeError("Dictionary service is not loaded")

    dictionary_service.add_word(payload.word, frequency=1)

    return {"status": "ok", "word": payload.word}
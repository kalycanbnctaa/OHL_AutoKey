from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.autocomplete import router as autocomplete_router
from app.api.routes.bigram import router as bigram_router
from app.api.routes.dictionary import router as dictionary_router
from app.api.routes.segmentation import router as segmentation_router
from app.api.routes.smart_trim import router as smart_trim_router
from app.api.routes.spellcheck import router as spellcheck_router
from app.api.routes.system import router as system_router
from app.config import (
    APP_DESCRIPTION,
    APP_NAME,
    APP_VERSION,
    BACKEND_HOST,
    BACKEND_PORT,
    FRONTEND_URL,
)
from app.services.dictionary_service import DictionaryService


@asynccontextmanager
async def lifespan(app: FastAPI):
    dictionary_service = DictionaryService()
    dictionary_service.load()
    app.state.dictionary_service = dictionary_service
    yield


app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    description=APP_DESCRIPTION,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

app.include_router(system_router)
app.include_router(autocomplete_router)
app.include_router(spellcheck_router)
app.include_router(dictionary_router)
app.include_router(segmentation_router)
app.include_router(smart_trim_router)
app.include_router(bigram_router)


@app.get("/")
async def root() -> dict[str, str]:
    return {"application": APP_NAME, "version": APP_VERSION, "status": "ok"}


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=BACKEND_HOST,
        port=BACKEND_PORT,
        reload=True,
    )
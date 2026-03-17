from fastapi import FastAPI
from app.api.v1_router import router as api_router
from app.core.config import settings

app = FastAPI(title=settings.APP_NAME, version=settings.VERSION)

# Health-check для високого рівня
@app.get("/health", tags=["System"])
async def health_check():
    return {"status": "ok", "env": settings.ENV}

app.include_router(api_router, prefix="/api/v1")
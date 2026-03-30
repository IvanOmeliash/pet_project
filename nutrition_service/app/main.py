from fastapi import FastAPI
from app.api.v1_router import router as api_router
from app.core.config import settings
from fastapi import Request
from fastapi.responses import JSONResponse
from datetime import datetime
from app.core.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.APP_NAME, version=settings.VERSION)

# Health-check для високого рівня
@app.get("/health", tags=["System"])
async def health_check():
    return {"status": "ok", "env": settings.ENV}

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "timestamp": datetime.now().isoformat(),
            "status": 500,
            "message": "Internal Server Error",
            "path": request.url.path
        }
    )

@app.exception_handler(404)
async def not_found_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=404,
        content={
            "timestamp": datetime.now().isoformat(),
            "status": 404,
            "message": str(exc.detail) if hasattr(exc, 'detail') else "Not Found",
            "path": request.url.path
        }
    )

app.include_router(api_router, prefix="/api/v1")
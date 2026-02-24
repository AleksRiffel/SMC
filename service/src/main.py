"""Главный файл FastAPI приложения"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from src.core.config import settings
from src.api.routes import router as documents_router

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(documents_router, prefix="/api/v1")

os.makedirs(settings.GENERATED_DIR, exist_ok=True)
os.makedirs(settings.UPLOADS_DIR, exist_ok=True)

if os.path.exists(settings.GENERATED_DIR):
    app.mount("/generated", StaticFiles(directory=settings.GENERATED_DIR), name="generated")

@app.get("/")
async def root():
    return {
        "message": "SMC Service API",
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": settings.APP_VERSION}
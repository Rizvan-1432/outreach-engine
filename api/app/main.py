from app.config import settings
from app.routers import email, leads, telegram
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title=settings.app_name,
    description="API для outreach-автоматизации: email DNS, enrichment лидов, Telegram/n8n",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(email.router, prefix="/api/v1")
app.include_router(leads.router, prefix="/api/v1")
app.include_router(telegram.router, prefix="/api/v1")


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "service": settings.app_name}

from __future__ import annotations

from pydantic import BaseModel, Field

from app.config import settings
from app.services.telegram_notifier import send_telegram_message
from fastapi import APIRouter, Header, HTTPException

router = APIRouter(prefix="/telegram", tags=["telegram"])


class NotifyRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=4096)
    secret: str | None = None


class WebhookPayload(BaseModel):
    event: str
    data: dict = Field(default_factory=dict)


@router.post("/notify")
async def notify(body: NotifyRequest) -> dict:
    """Отправка алерта в Telegram — для n8n webhook или ручных тестов."""
    if settings.n8n_webhook_secret and body.secret != settings.n8n_webhook_secret:
        raise HTTPException(status_code=403, detail="Invalid secret")
    return await send_telegram_message(body.message)


@router.post("/webhook")
async def n8n_webhook(
    payload: WebhookPayload,
    x_webhook_secret: str | None = Header(default=None),
) -> dict:
    """Приём событий из n8n (email alert, новый лид и т.д.)."""
    if settings.n8n_webhook_secret and x_webhook_secret != settings.n8n_webhook_secret:
        raise HTTPException(status_code=403, detail="Invalid webhook secret")

    text = (
        f"<b>Outreach Engine</b>\n"
        f"Event: <code>{payload.event}</code>\n"
        f"Data: <pre>{payload.data}</pre>"
    )
    return await send_telegram_message(text)

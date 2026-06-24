import httpx

from app.config import settings


async def send_telegram_message(text: str, parse_mode: str = "HTML") -> dict:
    token = settings.telegram_bot_token
    chat_id = settings.telegram_chat_id
    if not token or not chat_id:
        return {"ok": False, "error": "TELEGRAM_BOT_TOKEN или TELEGRAM_CHAT_ID не заданы"}

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": text, "parse_mode": parse_mode}

    async with httpx.AsyncClient(timeout=15.0) as client:
        response = await client.post(url, json=payload)
        data = response.json()
        if not response.is_success:
            return {"ok": False, "error": data}
        return {"ok": True, "result": data.get("result")}

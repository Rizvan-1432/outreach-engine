from __future__ import annotations

from pydantic import BaseModel, Field

from app.services.dns_checker import check_domain_deliverability
from fastapi import APIRouter

router = APIRouter(prefix="/email", tags=["email"])


class DomainCheckRequest(BaseModel):
    domain: str = Field(..., examples=["example.com"])


@router.post("/check-domain")
def check_domain(body: DomainCheckRequest) -> dict:
    """Проверка MX, SPF, DMARC — базовая диагностика email-инфраструктуры."""
    return check_domain_deliverability(body.domain).to_dict()


@router.get("/check-domain/{domain}")
def check_domain_get(domain: str) -> dict:
    return check_domain_deliverability(domain).to_dict()

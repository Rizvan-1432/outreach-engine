from __future__ import annotations

from pydantic import BaseModel, Field

from app.services.lead_enrichment import LeadInput, enrich_lead
from fastapi import APIRouter

router = APIRouter(prefix="/leads", tags=["leads"])


class LeadEnrichRequest(BaseModel):
    full_name: str = Field(..., min_length=2)
    company: str | None = None
    email: str | None = None
    linkedin_url: str | None = None
    title: str | None = None


class LeadBatchRequest(BaseModel):
    leads: list[LeadEnrichRequest]


@router.post("/enrich")
def enrich_single(body: LeadEnrichRequest) -> dict:
    """
    Обогащение лида: валидация LinkedIn URL, эвристический email-guess, теги для CRM/n8n.
    Без скрейпинга — готово к подключению внешних enrichment API.
    """
    lead = enrich_lead(
        LeadInput(
            full_name=body.full_name,
            company=body.company,
            email=body.email,
            linkedin_url=body.linkedin_url,
            title=body.title,
        )
    )
    return lead.to_dict()


@router.post("/enrich/batch")
def enrich_batch(body: LeadBatchRequest) -> dict:
    enriched: list[dict] = []
    for item in body.leads:
        lead = enrich_lead(
            LeadInput(
                full_name=item.full_name,
                company=item.company,
                email=item.email,
                linkedin_url=item.linkedin_url,
                title=item.title,
            )
        )
        enriched.append(lead.to_dict())
    return {"count": len(enriched), "leads": enriched}

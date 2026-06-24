from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, field


LINKEDIN_PROFILE_RE = re.compile(
    r"^https?://(www\.)?linkedin\.com/in/[\w\-%.]+/?$", re.IGNORECASE
)


@dataclass
class LeadInput:
    full_name: str
    company: str | None = None
    email: str | None = None
    linkedin_url: str | None = None
    title: str | None = None


@dataclass
class EnrichedLead:
    full_name: str
    company: str | None
    email: str | None
    linkedin_url: str | None
    title: str | None
    email_guess: str | None = None
    linkedin_slug: str | None = None
    tags: list[str] = field(default_factory=list)
    confidence: int = 0
    source: str = "local-heuristics"

    def to_dict(self) -> dict:
        return {
            "full_name": self.full_name,
            "company": self.company,
            "email": self.email,
            "linkedin_url": self.linkedin_url,
            "title": self.title,
            "email_guess": self.email_guess,
            "linkedin_slug": self.linkedin_slug,
            "tags": self.tags,
            "confidence": self.confidence,
            "source": self.source,
        }


def _slugify_name(name: str) -> str:
    parts = re.sub(r"[^a-zA-Zа-яА-ЯёЁ\s\-]", "", name).lower().split()
    if len(parts) >= 2:
        return f"{parts[0]}.{parts[-1]}"
    return parts[0] if parts else "contact"


def _guess_email(name: str, company: str | None) -> str | None:
    if not company:
        return None
    domain = re.sub(r"[^a-z0-9\-]", "", company.lower().replace(" ", ""))
    if not domain or len(domain) < 2:
        return None
    slug = _slugify_name(name)
    return f"{slug}@{domain}.com"


def enrich_lead(lead: LeadInput) -> EnrichedLead:
    """
    Локальное обогащение лида без скрейпинга LinkedIn.
    Для продакшена подключают Apollo, Hunter, Clearbit и т.п. через API.
    """
    tags: list[str] = []
    confidence = 50

    linkedin_slug = None
    if lead.linkedin_url:
        if LINKEDIN_PROFILE_RE.match(lead.linkedin_url.strip()):
            linkedin_slug = lead.linkedin_url.rstrip("/").split("/")[-1]
            tags.append("linkedin-valid-url")
            confidence += 20
        else:
            tags.append("linkedin-invalid-url")
            confidence -= 15

    email = lead.email
    email_guess = None
    if email:
        tags.append("email-provided")
        confidence += 15
    elif lead.company:
        email_guess = _guess_email(lead.full_name, lead.company)
        if email_guess:
            tags.append("email-guessed")
            confidence += 5

    if lead.company:
        tags.append("company-known")
        confidence += 10
    if lead.title:
        tags.append("title-known")
        confidence += 5

    dedup_key = hashlib.sha256(
        f"{lead.full_name}|{lead.company}|{lead.linkedin_url}".encode()
    ).hexdigest()[:12]
    tags.append(f"dedup:{dedup_key}")

    confidence = max(0, min(100, confidence))

    return EnrichedLead(
        full_name=lead.full_name,
        company=lead.company,
        email=email,
        linkedin_url=lead.linkedin_url,
        title=lead.title,
        email_guess=email_guess,
        linkedin_slug=linkedin_slug,
        tags=tags,
        confidence=confidence,
    )

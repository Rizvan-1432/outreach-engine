from __future__ import annotations

import dns.exception
import dns.resolver
from dataclasses import dataclass, field


@dataclass
class DnsCheckResult:
    domain: str
    mx_records: list[str] = field(default_factory=list)
    spf_record: str | None = None
    dmarc_record: str | None = None
    issues: list[str] = field(default_factory=list)
    score: int = 0

    def to_dict(self) -> dict:
        return {
            "domain": self.domain,
            "mx_records": self.mx_records,
            "spf_record": self.spf_record,
            "dmarc_record": self.dmarc_record,
            "issues": self.issues,
            "score": self.score,
            "status": "ok" if self.score >= 70 else "warning" if self.score >= 40 else "critical",
        }


def _query_txt(name: str) -> list[str]:
    try:
        answers = dns.resolver.resolve(name, "TXT")
        return [b"".join(r.strings).decode("utf-8", errors="replace") for r in answers]
    except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, dns.exception.DNSException):
        return []


def check_domain_deliverability(domain: str) -> DnsCheckResult:
    domain = domain.strip().lower().removeprefix("http://").removeprefix("https://")
    if "@" in domain:
        domain = domain.split("@", 1)[1]
    domain = domain.split("/", 1)[0]

    result = DnsCheckResult(domain=domain)
    score = 100

    try:
        mx_answers = dns.resolver.resolve(domain, "MX")
        result.mx_records = sorted(
            f"{r.preference} {str(r.exchange).rstrip('.')}" for r in mx_answers
        )
    except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, dns.exception.DNSException):
        result.issues.append("MX-записи не найдены — домен не может принимать почту")
        score -= 40

    txt_records = _query_txt(domain)
    spf = next((r for r in txt_records if r.lower().startswith("v=spf1")), None)
    if spf:
        result.spf_record = spf
        if "~all" in spf or "-all" in spf:
            pass
        elif "?all" in spf or "+all" in spf:
            result.issues.append("SPF: слабая политика all (рекомендуется ~all или -all)")
            score -= 10
    else:
        result.issues.append("SPF-запись не найдена")
        score -= 25

    dmarc_records = _query_txt(f"_dmarc.{domain}")
    dmarc = next((r for r in dmarc_records if r.lower().startswith("v=dmarc1")), None)
    if dmarc:
        result.dmarc_record = dmarc
        if "p=reject" not in dmarc.lower() and "p=quarantine" not in dmarc.lower():
            result.issues.append("DMARC: политика p=none — слабая защита доставляемости")
            score -= 10
    else:
        result.issues.append("DMARC-запись не найдена")
        score -= 20

    if not result.mx_records:
        result.issues.append("Проверьте DNS у регистратора и время распространения (TTL)")

    result.score = max(0, min(100, score))
    return result

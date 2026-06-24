#!/usr/bin/env python3
"""CLI: проверка email-инфраструктуры домена."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "api"))

from app.services.dns_checker import check_domain_deliverability


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python scripts/check_domain.py example.com")
        sys.exit(1)

    result = check_domain_deliverability(sys.argv[1])
    data = result.to_dict()
    print(f"Domain: {data['domain']}")
    print(f"Score:  {data['score']}/100 ({data['status']})")
    print(f"MX:     {', '.join(data['mx_records']) or '—'}")
    print(f"SPF:    {data['spf_record'] or '—'}")
    print(f"DMARC:  {data['dmarc_record'] or '—'}")
    if data["issues"]:
        print("Issues:")
        for issue in data["issues"]:
            print(f"  - {issue}")


if __name__ == "__main__":
    main()

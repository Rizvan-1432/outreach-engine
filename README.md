# Outreach Engine

Pet-проект под **outreach-автоматизацию**: email DNS, enrichment лидов, Telegram-алерты, n8n workflows.

**Автор:** Бакаев Ризван

## Стек

| Слой | Технологии |
|------|------------|
| API | Python 3.12, FastAPI, dnspython, httpx |
| Автоматизация | n8n (Docker) |
| Интеграции | Telegram Bot API, webhooks |

## Возможности

- **Email infrastructure** — проверка MX, SPF, DMARC, score доставляемости
- **Lead enrichment** — валидация LinkedIn URL, email-guess, теги для CRM (без скрейпинга)
- **Telegram** — уведомления и webhook для n8n
- **n8n** — готовые workflow: health-check домена, pipeline обогащения лидов

## Быстрый старт

### 1. API локально

```bash
cd api
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp ../.env.example ../.env
# заполните TELEGRAM_BOT_TOKEN и TELEGRAM_CHAT_ID при необходимости
uvicorn app.main:app --reload --port 8000
```

Документация: http://localhost:8000/docs

### 2. Docker (API + n8n)

```bash
cp .env.example .env
docker compose up --build
```

- API: http://localhost:8000  
- n8n: http://localhost:5678  

Импортируйте workflow из `n8n/workflows/`.

### 3. Деплой онлайн (Render / Railway)

Пошаговая инструкция: **[DEPLOY.md](./DEPLOY.md)**

- **Render** — API бесплатно (рекомендуется для старта)
- **Railway** — API или полный стек API + n8n
- **Vercel** — не подходит для FastAPI + n8n без доработок

### 4. CLI

```bash
python scripts/check_domain.py google.com
```

## API

| Method | Endpoint | Описание |
|--------|----------|----------|
| GET | `/health` | Health check |
| GET/POST | `/api/v1/email/check-domain` | MX, SPF, DMARC |
| POST | `/api/v1/leads/enrich` | Обогащение лида |
| POST | `/api/v1/leads/enrich/batch` | Пакетное обогащение |
| POST | `/api/v1/telegram/notify` | Алерт в Telegram |
| POST | `/api/v1/telegram/webhook` | Webhook из n8n |

## Примеры

```bash
# Проверка домена
curl http://localhost:8000/api/v1/email/check-domain/gmail.com

# Обогащение лида
curl -X POST http://localhost:8000/api/v1/leads/enrich \
  -H "Content-Type: application/json" \
  -d '{"full_name":"Иван Петров","company":"acme","linkedin_url":"https://linkedin.com/in/ivan-petrov"}'
```

## Для портфолио

Демонстрирует навыки из вакансий outreach/automation:
- Python + API
- email deliverability (DNS)
- n8n автоматизация
- Telegram интеграции
- этичный подход к LinkedIn (enrichment без скрейпинга)

## Дальше

- [ ] Подключить Hunter / Apollo API для реального enrichment
- [ ] Warm-up tracker для email-доменов
- [ ] PostgreSQL для хранения лидов
- [ ] Экспорт в CSV / Google Sheets из n8n

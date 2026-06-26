# Деплой Outreach Engine онлайн

Проект состоит из **API (FastAPI)** и **n8n**. На Vercel весь стек не поднять — используйте **Render** или **Railway**.

| Компонент | Render | Railway | Vercel |
|-----------|--------|---------|--------|
| API (FastAPI) | ✅ | ✅ | ⚠️ только через serverless-доработку |
| n8n | ❌ | ✅ (Docker + volume) | ❌ |

---

## Вариант 1 — API на Render (самый простой, бесплатно)

### Шаг 1. Залейте код на GitHub

Репозиторий: https://github.com/Rizvan-1432/outreach-engine

### Шаг 2. Создайте аккаунт Render

1. Откройте https://render.com и войдите через GitHub.
2. **New** → **Blueprint**.
3. Подключите репозиторий `outreach-engine`.
4. Render подхватит файл `render.yaml` из корня.

### Шаг 3. Переменные окружения

В панели сервиса **Environment**:

| Переменная | Значение |
|------------|----------|
| `TELEGRAM_BOT_TOKEN` | токен от @BotFather (опционально) |
| `TELEGRAM_CHAT_ID` | ваш chat id (опционально) |
| `N8N_WEBHOOK_SECRET` | любой секрет, например `my-secret-123` |

### Шаг 4. Deploy

Нажмите **Deploy**. Через 2–5 минут получите URL:

```
https://outreach-engine-api.onrender.com
```

### Шаг 5. Проверка

```bash
curl https://ВАШ-URL.onrender.com/health
curl https://ВАШ-URL.onrender.com/api/v1/email/check-domain/gmail.com
```

Документация: `https://ВАШ-URL.onrender.com/docs`

> **Free tier:** сервис «засыпает» после простоя; первый запрос может занять 30–60 сек.

---

## Вариант 2 — API на Railway

### Шаг 1. Аккаунт Railway

1. https://railway.app → Login with GitHub.
2. **New Project** → **Deploy from GitHub repo**.
3. Выберите `outreach-engine`.

### Шаг 2. Root Directory

В настройках сервиса:

- **Root Directory:** `api`
- Railway использует `api/railway.toml` и `api/Dockerfile`.

### Шаг 3. Переменные

**Variables** → добавьте:

```
TELEGRAM_BOT_TOKEN=
TELEGRAM_CHAT_ID=
N8N_WEBHOOK_SECRET=change-me
```

### Шаг 4. Домен

**Settings** → **Networking** → **Generate Domain**.

Пример: `outreach-engine-api-production.up.railway.app`

### Шаг 5. Проверка

```bash
curl https://ВАШ-ДОМЕН.railway.app/health
```

---

## Вариант 3 — API + n8n на Railway (полный стек)

### Шаг 1. Новый проект из docker-compose

1. Railway → **New Project** → **Empty Project**.
2. **Add Service** → **GitHub Repo** → `outreach-engine`.
3. В настройках сервиса выберите деплой через **Docker Compose** (файл `docker-compose.yml`).

### Шаг 2. Переменные для n8n

Добавьте в сервис n8n:

```
N8N_HOST=ваш-домен-n8n.up.railway.app
N8N_PROTOCOL=https
WEBHOOK_URL=https://ваш-домен-n8n.up.railway.app/
```

### Шаг 3. Volume для n8n

**Volumes** → mount `/home/node/.n8n` — чтобы workflow и настройки сохранялись.

### Шаг 4. Публичные домены

Сгенерируйте домен для **api** и **n8n** в Networking.

### Шаг 5. Обновите workflow

В импортированных workflow замените URL:

| Было (локально) | Стало (онлайн) |
|-----------------|----------------|
| `http://api:8000` | `https://ВАШ-API-ДОМЕН` |

Файлы для справки: `n8n/workflows/email-domain-health.json`, `lead-enrichment-pipeline.json`.

### Шаг 6. Импорт workflow в n8n

1. Откройте `https://ВАШ-N8N-ДОМЕН`.
2. Создайте аккаунт владельца.
3. **Workflows** → **Import from File** → файлы из `n8n/workflows/`.
4. Включите **Active**.

---

## n8n без своего сервера

Если не хотите поднимать n8n сами:

1. Зарегистрируйтесь на https://n8n.io/cloud
2. Импортируйте workflow
3. В HTTP-нодах укажите URL вашего API на Render/Railway

---

## Что указать в портфолио

После деплоя добавьте в README и резюме:

```
API (live): https://outreach-engine-api.onrender.com/docs
GitHub:     https://github.com/Rizvan-1432/outreach-engine
```

---

## Частые проблемы

| Проблема | Решение |
|----------|---------|
| 502 / сервис не отвечает | Подождите 1–2 мин после деплоя; на Render free — «пробуждение» |
| Telegram не шлёт | Проверьте `TELEGRAM_BOT_TOKEN` и `TELEGRAM_CHAT_ID` |
| n8n не видит API | Замените `http://api:8000` на публичный HTTPS URL |
| Webhook 401 | `N8N_WEBHOOK_SECRET` в `.env` API = заголовок в workflow |

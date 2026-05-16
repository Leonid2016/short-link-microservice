# Fresh microservices v1

Это чистая greenfield-версия на базе логики монолита.

Старая БД не используется вообще:
- ничего не мигрируем
- ничего не импортируем
- старый монолит можно не запускать
- поднимаются только новые сервисы и три новые БД

## Состав

- `auth-service` — регистрация, логин, JWT, список пользователей
- `links-service` — создание ссылок, список ссылок, включение/выключение, редирект
- `analytics-service` — сбор кликов и статистика
- `gateway` — сохраняет старые frontend endpoint'ы `/api/*` и `/s/*`
- `frontend` — твой UI

## Что сохранено из монолита

- `POST /api/auth/login`
- `POST /api/auth/register`
- `GET /api/admin/users`
- `POST /api/links`
- `GET /api/links`
- `PATCH /api/links/<code>`
- `GET /api/links/<code>/stats`
- `GET /s/<code>`

## Важное архитектурное решение

Чтобы не делать кросс-БД join между auth и links, в `links-service` сохраняется:
- `owner_user_id`
- `owner_email_snapshot`

Это позволяет сохранить текущий админский фильтр по email без обращения к старой БД.

## Как разложить рядом с текущими файлами

В корне проекта должны быть папки:

```text
project/
  auth-service/
  links-service/
  analytics-service/
  shared/
  deploy/
  frontend/
```

В `frontend/` нужно положить твои обычные frontend-файлы проекта плюс два файла из этого архива:
- `Dockerfile`
- `nginx.conf`

## Запуск

Из папки `deploy`:

```bash
docker compose up --build
```

После старта:
- приложение: `http://localhost`
- логин админа: `admin@example.com`
- пароль: `123`

## Очистка

```bash
docker compose down -v
```

## Что дальше логично делать этапом 2

1. добавить healthcheck'и в compose
2. вынести shared-утилиты в отдельный pip package
3. закрыть внутренние endpoint'ы внутренней сетью или internal auth
4. добавить retry/wait-for-db
5. добавить e2e smoke tests

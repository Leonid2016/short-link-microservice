# URL Shortener

Небольшой веб-сервис для сокращения ссылок с авторизацией, статистикой переходов и административной панелью.

## Описание проекта

URL Shortener позволяет создавать короткие ссылки для длинных URL-адресов. Пользователь может зарегистрироваться, войти в систему, создавать и просматривать свои ссылки, а также смотреть статистику переходов. Для администратора доступен просмотр пользователей и управление активностью ссылок.

Проект состоит из backend-части на Flask, frontend-части на Vue 3 и базы данных PostgreSQL. Запуск выполняется через Docker Compose.

## Возможности

- создание коротких ссылок;
- редирект по короткому коду;
- регистрация и авторизация пользователей;
- JWT-аутентификация;
- создание ссылок без регистрации в гостевом режиме;
- возможность задать пользовательский alias для ссылки;
- установка срока действия ссылки;
- просмотр списка созданных ссылок;
- сбор статистики переходов;
- просмотр статистики по дням, источникам и последним кликам;
- административная панель пользователей;
- запуск проекта через Docker Compose.

## Технологии

### Backend

- Python
- Flask
- PostgreSQL
- psycopg
- JWT
- Flask-CORS

### Frontend

- Vue 3
- Vite
- Vue Router
- Tailwind CSS

### Инфраструктура

- Docker
- Docker Compose
- Nginx
- PostgreSQL 16

## Запуск проекта

Склонируйте репозиторий:

```bash
git clone https://github.com/username/repository-name.git
cd repository-name
```

Запустите проект:

```bash
docker compose up --build
```

После запуска приложение будет доступно по адресу:

```text
http://localhost:8080
```

Backend API доступен через прокси:

```text
http://localhost:8080/api
```

## Основные страницы

| Страница | Описание |
|---|---|
| `/` | Главная страница |
| `/login` | Вход пользователя |
| `/register` | Регистрация пользователя |
| `/links` | Список созданных ссылок |
| `/stats/:code` | Статистика конкретной ссылки |
| `/admin/users` | Административная панель пользователей |

## API

Основные маршруты API:

```http
POST   /api/auth/register
POST   /api/auth/login
POST   /api/links
GET    /api/links
GET    /api/links/:code/stats
PATCH  /api/links/:code
GET    /api/admin/users
```

Редирект по короткой ссылке:

```http
GET /s/:code
```

## Переменные окружения

Пример переменных окружения для backend:

```env
DATABASE_URL=postgresql://urlshort_user:urlshort_pass@postgres:5432/urlshort
BASE_URL=http://localhost:8080
JWT_SECRET=dev
```

При запуске через Docker Compose эти значения уже указаны в `docker-compose.yml`.

## Создание администратора

Для создания администратора можно использовать скрипт:

```bash
python create_admin.py
```

По умолчанию создаётся пользователь:

```text
email: admin@t.com
password: 123
```

## Структура проекта

```text
project/
├── backend/
│   ├── app/
│   │   ├── auth.py
│   │   ├── config.py
│   │   ├── db.py
│   │   ├── models.py
│   │   ├── routes_api.py
│   │   ├── routes_redirect.py
│   │   └── utils.py
│   ├── create_admin.py
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   ├── api.js
│   │   ├── authStore.js
│   │   ├── main.js
│   │   └── router.js
│   ├── nginx.conf
│   └── Dockerfile
├── docker-compose.yml
└── README.md
```

## Примечание

Проект разработан в учебных целях и демонстрирует работу с Flask API, Vue frontend, PostgreSQL, JWT-авторизацией и контейнеризацией через Docker.

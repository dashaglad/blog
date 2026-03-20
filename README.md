# Blog API

## Оглавление
- [Описание](#описание)
- [Запуск проекта](#запуск-проекта)
- [Структура проекта](#структура-проекта)
- [Кеширование](#кеширование)
- [Запуск тестов](#запуск-тестов)

## Описание

Blog API — это backend на базе **FastAPI**, который хранит сущности `Post` в **PostgreSQL** и использует **Redis** для кеширования популярных постов `GET /posts/{id}`.

В проекте предусмотрены:
- Docker Compose окружение (app + db + redis)
- отдельный сервис для тестов (`profile: tests`)
- кеширование с инвалидированием на `PATCH/DELETE`

---

## Запуск проекта

Для начала работы с этим проектом вам потребуется выполнить несколько шагов.

#### 1. Клонируйте этот репозиторий на ваш компьютер с помощью следующей команды:

```bash
git clone https://github.com/dashaglad/blog.git blog
```

#### 2. Перейдите в директорию проекта:

```bash
cd blog
```

#### 3. Скопируйте пример файла окружения

```bash
cp .env.example .env
```


### 2. Контейнеры в `docker-compose.yml`

В `docker-compose.yml` используются следующие сервисы:

- `db` — PostgreSQL для основного окружения
- `db_tests` — PostgreSQL для тестов (`profile: tests`)
- `redis` — Redis для кеширования и тестов
- `app` — основной контейнер с API (FastAPI + Uvicorn)
- `tests` — контейнер для запуска `pytest` (`profile: tests`)

---

### 3. Запуск Docker

Для первого запуска выполните сборку:

```bash
docker compose up --build -d
```

Дальше можно запускать без пересборки:

```bash
docker compose up -d
```

Документация доступна по адресу:
`http://localhost:8000/docs`

Эндпоинты:
- `POST /posts/`
- `GET /posts/`
- `GET /posts/{post_id}`
- `PATCH /posts/{post_id}`
- `DELETE /posts/{post_id}`

---

## Структура проекта

Ключевые директории:

- `app/main.py` — создание приложения FastAPI и подключение роутов
- `app/api/` — HTTP API (например, `posts.py`)
- `app/core/` — инфраструктура:
  - `db.py` — движок SQLAlchemy и `get_db()`
  - `redis.py` — клиент Redis
  - `config.py` — чтение env через `pydantic-settings`
- `app/models/` — модели SQLAlchemy (например, `Post`)
- `app/repositories/` — слой доступа к данным (CRUD)
- `app/services/` — бизнес-логика и кеширование (`PostService`)
- `app/schemas/` — Pydantic схемы запросов/ответов
- `app/utils/` — утилиты (например, `Cache`)
- `tests/` — тесты (например, `test_post_cache.py`)

---

## Кеширование

Кеширование сделано через Redis и обёртку `app/utils/cache.py`.

Принцип:
- Для каждого поста используется ключ вида: `post:{post_id}`
- При `GET /posts/{id}` сначала делается попытка чтения из кеша
- Если в кеше есть данные — ответ формируется без запроса в БД
- TTL кеша задаётся через `CACHE_TTL`

Инвалидация:
- При `PATCH /posts/{id}` выполняется `Cache.delete("post:{id}")`
- При `DELETE /posts/{id}` также выполняется `Cache.delete("post:{id}")`

---

## Запуск тестов

Тесты используют отдельную Postgres базу.

Перед запуском убедитесь, что в `.env` выставлены:
- `POSTGRES_DB_TEST` / `DATABASE_URL_TEST`
- `REDIS_URL_TEST`

Запуск:

```bash
docker compose --profile tests run --rm tests
```

Тест проверяет, что:
- после первого `GET /posts/{id}` данные появляются в Redis
- на повторном `GET` запрос в БД не выполняется

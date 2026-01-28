# Онлайн-школа английского: 300+ студентов без куратора

> Интерактивный кейс-портфолио, демонстрирующий AI-автоматизацию образовательной платформы на базе GetCourse.

## Результаты проекта

| Метрика | До | После | Изменение |
|---------|-----|-------|-----------|
| Retention | 85% | 92% | **+7%** |
| Новых студентов | - | +45/мес | **+45** |
| Кураторов | 3 | 1 | **-2 человека** |
| Время ответа | 2-4 часа | 2-3 сек | **-99.9%** |
| AI resolution rate | 0% | 90% | **+90%** |
| ROI | - | 30 дней | - |
| Годовая прибыль | - | +4.4 млн руб | - |

---

## Описание проекта

### Проблема клиента

Онлайн-школа английского языка на платформе GetCourse столкнулась с проблемой масштабирования:

- **100+ сообщений в день** от студентов
- **30+ домашних заданий** требуют проверки ежедневно
- **40-60 часов в неделю** уходит на поддержку
- **15% студентов отваливаются** из-за долгого ожидания ответов
- **Убыток 180к руб/месяц** от потерянных студентов

### Решение

Комплексная AI-автоматизация образовательного процесса:

1. **AI-ассистент 24/7** — отвечает на 90% вопросов студентов за 2-3 секунды
2. **Автопроверка домашних заданий** — мгновенная обратная связь с детальным разбором
3. **Умный дашборд куратора** — приоритизация студентов по риску отвала
4. **Система раннего предупреждения** — автоматическое выявление отстающих

### Интерактивные секции кейса

| # | Секция | Описание |
|---|--------|----------|
| 1 | Исходная проблема | Скриншоты перегрузки, метрики "до" |
| 2 | Решение | Компоненты системы, timeline внедрения |
| 3 | AI-ассистент | **Работающий чат** — можно задать вопрос |
| 4 | Личный кабинет | Интерактивный прогресс студента |
| 5 | Дашборд куратора | Фильтры, real-time уведомления |
| 6 | Результаты | Анимированные графики retention/прибыли |
| 7 | Финансы | ROI, окупаемость, годовой результат |

---

## Технологический стек

### Backend

| Технология | Версия | Назначение |
|------------|--------|------------|
| **Python** | 3.12 | Язык программирования |
| **FastAPI** | 0.115+ | Web-фреймворк (async) |
| **Pydantic** | 2.x | Валидация данных, настройки |
| **SQLAlchemy** | 2.x | ORM (async) |
| **Alembic** | 1.x | Миграции БД |
| **python-jose** | 3.x | JWT авторизация |
| **httpx** | 0.27+ | Async HTTP клиент |
| **Granian** | 1.x | ASGI сервер (Rust-based) |

#### Качество кода

| Инструмент | Назначение |
|------------|------------|
| **Ruff** | Линтер + форматтер (замена flake8, black, isort) |
| **mypy** | Статическая типизация |
| **pytest** | Тестирование |
| **pytest-asyncio** | Async тесты |
| **pytest-cov** | Покрытие кода |

---

### Frontend

| Технология | Версия | Назначение |
|------------|--------|------------|
| **Vue.js** | 3.5+ | UI фреймворк (Composition API) |
| **TypeScript** | 5.x | Типизация |
| **Vite** | 6.x | Сборщик |
| **TailwindCSS** | 3.x | Утилитарные стили |
| **Vue Router** | 4.x | Роутинг |
| **Pinia** | 2.x | State management |
| **Axios** | 1.x | HTTP клиент |

#### UI компоненты

| Библиотека | Назначение |
|------------|------------|
| **Lucide Vue** | Иконки |
| **Chart.js** | Графики (retention, прибыль) |
| **@twa-dev/sdk** | Telegram Mini App SDK |

---

### База данных

| Технология | Версия | Назначение |
|------------|--------|------------|
| **PostgreSQL** | 16 | Основная БД |
| **pgvector** | 0.7+ | Векторный поиск (AI knowledge base) |
| **Redis** | 7 | Кеширование, сессии, очереди |

---

### Инфраструктура

| Технология | Назначение |
|------------|------------|
| **Docker** | Контейнеризация |
| **Nginx** | Reverse proxy, статика frontend |
| **MinIO** | S3-совместимое хранилище (сертификаты, файлы) |
| **Directus** | Админ-панель для БД (просмотр/редактирование) |

---

### CI/CD & Deploy

```
Local Development → GitHub Push → Coolify Auto-Deploy
```

| Этап | Инструмент |
|------|------------|
| Локальная разработка | Docker Compose |
| Task runner | **just** (justfile) |
| Репозиторий | GitHub |
| Деплой | **Coolify** (self-hosted PaaS) |
| SSL | Auto (Let's Encrypt через Coolify) |

---

### Интеграции

| Сервис | Назначение |
|--------|------------|
| **OpenAI API** | GPT-4o-mini для AI-ассистента |
| **Telegram Bot API** | Авторизация через Telegram User ID |
| **GetCourse API** | Синхронизация студентов (mock для демо) |

---

## Авторизация

**Telegram Mini App** — безпарольная авторизация:

1. Пользователь открывает Mini App в Telegram
2. Frontend получает `initData` из Telegram SDK
3. Backend валидирует подпись через HMAC-SHA256
4. Создается/обновляется пользователь по `telegram_id`
5. Возвращается JWT токен

```
Telegram App → initData → Backend validates → JWT token → Authorized
```

---

## Структура проекта

```
case-2-education/
├── backend/                 # FastAPI приложение
│   ├── app/
│   │   ├── api/            # Роуты (auth, students, chat, etc.)
│   │   ├── models/         # SQLAlchemy модели
│   │   ├── schemas/        # Pydantic схемы
│   │   ├── services/       # Бизнес-логика
│   │   ├── integrations/   # Внешние API (OpenAI, Telegram)
│   │   └── db/             # Сессия, миграции
│   ├── tests/
│   ├── pyproject.toml
│   └── Dockerfile
│
├── frontend/               # Vue.js приложение
│   ├── src/
│   │   ├── components/     # Vue компоненты
│   │   │   ├── sections/   # 7 секций кейса
│   │   │   ├── chat/       # AI чат
│   │   │   ├── dashboard/  # Дашборд куратора
│   │   │   └── charts/     # Графики
│   │   ├── stores/         # Pinia stores
│   │   ├── composables/    # Vue composables
│   │   └── api/            # API клиенты
│   ├── package.json
│   └── Dockerfile
│
├── docker/
│   ├── docker-compose.yml  # Локальная разработка
│   └── nginx/
│
├── justfile                # Task runner
├── .env.example
├── ARCHITECTURE.md         # Детальная архитектура
└── README.md               # Этот файл
```

---

## Быстрый старт

### Требования

- Docker & Docker Compose
- just (task runner): `cargo install just` или `brew install just`
- Node.js 20+ (для локальной разработки frontend)
- Python 3.12+ (для локальной разработки backend)

### Запуск

```bash
# 1. Клонировать репозиторий
git clone https://github.com/your-repo/case-2-education.git
cd case-2-education

# 2. Скопировать переменные окружения
cp .env.example .env
# Заполнить TELEGRAM_BOT_TOKEN, OPENAI_API_KEY, etc.

# 3. Запустить все сервисы
just up

# 4. Применить миграции и загрузить демо-данные
just db-migrate
just db-seed

# 5. Открыть в браузере
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000/docs
# Directus: http://localhost:8055
# MinIO: http://localhost:9001
```

### Разработка

```bash
# Backend с hot reload
just dev-backend

# Frontend с hot reload
just dev-frontend

# Оба вместе
just dev

# Тесты
just test

# Линтинг
just lint

# Форматирование
just fmt
```

---

## API документация

После запуска backend доступна интерактивная документация:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

### Основные endpoints

| Метод | Endpoint | Описание |
|-------|----------|----------|
| POST | `/api/auth/telegram` | Авторизация через Telegram |
| GET | `/api/auth/me` | Текущий пользователь |
| GET | `/api/students` | Список студентов (фильтры) |
| GET | `/api/students/{id}/progress` | Прогресс студента |
| POST | `/api/chat/message` | Отправить вопрос AI |
| GET | `/api/dashboard/students` | Студенты с рисками |
| GET | `/api/metrics/retention` | Данные для графика retention |

---

## Лицензия

MIT

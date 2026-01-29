# Онлайн-школа английского: Архитектура проекта

## Обзор
Интерактивный кейс-портфолио, демонстрирующий AI-автоматизацию образовательной платформы.
**Результат**: 300+ студентов без куратора, +45% retention.

---

## 0. Инфраструктура и деплой

### CI/CD Pipeline
```
Local Development → GitHub Push → Coolify Auto-Deploy
```

**Процесс**:
1. Локальная разработка + тесты
2. `git push` в GitHub
3. Coolify webhook триггерит деплой
4. Coolify билдит Docker образы и деплоит

### Сервисы в продакшене (Coolify)

**Auto-deploy из GitHub** (наша зона ответственности):

| Сервис | Образ | Порт |
|--------|-------|------|
| Backend (FastAPI) | `Dockerfile` (backend/) | 8000 |
| Frontend (Vue) | `Dockerfile` (frontend/) | 80 |

**Развернуты вручную в Coolify** (инфраструктура):

| Сервис | Образ | Порт |
|--------|-------|------|
| PostgreSQL + pgvector | `pgvector/pgvector:pg16` | 5432 |
| Redis | `redis:7-alpine` | 6379 |
| Directus | `directus/directus:11` | 8055 |
| MinIO | `minio/minio` | 9000/9001 |

### Авторизация
**Telegram User ID** — простая авторизация без паролей:
- Frontend получает `telegram_user_id` из Telegram Mini App SDK
- Backend валидирует через `initData` от Telegram
- JWT токен содержит `telegram_id` как идентификатор

---

## 1. Структура проекта

```
case-2-education/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                    # FastAPI entrypoint
│   │   ├── config.py                  # Pydantic Settings
│   │   ├── dependencies.py            # DI контейнер
│   │   │
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── router.py              # Главный роутер
│   │   │   ├── auth.py                # /api/auth/* (Telegram auth)
│   │   │   ├── students.py            # /api/students/*
│   │   │   ├── lessons.py             # /api/lessons/*
│   │   │   ├── homework.py            # /api/homework/*
│   │   │   ├── chat.py                # /api/chat/* (AI assistant)
│   │   │   ├── dashboard.py           # /api/dashboard/*
│   │   │   └── metrics.py             # /api/metrics/*
│   │   │
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── user.py                # User (telegram_id based)
│   │   │   ├── student.py             # Student, StudentProgress
│   │   │   ├── course.py              # Course, Lesson, Test
│   │   │   ├── homework.py            # Homework, HomeworkSubmission
│   │   │   ├── chat.py                # ChatMessage, ChatSession
│   │   │   └── notification.py        # Notification
│   │   │
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py                # TelegramAuth, Token schemas
│   │   │   ├── student.py             # Pydantic schemas
│   │   │   ├── course.py
│   │   │   ├── homework.py
│   │   │   ├── chat.py
│   │   │   └── metrics.py
│   │   │
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── auth_service.py        # Telegram auth validation
│   │   │   ├── ai_assistant.py        # AI chat logic
│   │   │   ├── homework_checker.py    # Auto homework check
│   │   │   ├── notification_service.py
│   │   │   ├── risk_analyzer.py       # Student risk detection
│   │   │   └── metrics_calculator.py
│   │   │
│   │   ├── integrations/
│   │   │   ├── __init__.py
│   │   │   ├── telegram.py            # Telegram initData validation
│   │   │   ├── getcourse.py           # GetCourse API client
│   │   │   └── openai_client.py       # OpenAI/LLM client
│   │   │
│   │   └── db/
│   │       ├── __init__.py
│   │       ├── session.py             # SQLAlchemy async session
│   │       └── migrations/            # Alembic migrations
│   │
│   ├── tests/
│   │   ├── conftest.py
│   │   ├── test_auth.py
│   │   ├── test_chat.py
│   │   ├── test_students.py
│   │   └── test_homework.py
│   │
│   ├── pyproject.toml
│   ├── Dockerfile
│   └── .dockerignore
│
├── frontend/
│   ├── src/
│   │   ├── main.ts
│   │   ├── App.vue
│   │   │
│   │   ├── router/
│   │   │   └── index.ts               # Vue Router config
│   │   │
│   │   ├── stores/
│   │   │   ├── auth.ts                # Pinia: Telegram auth state
│   │   │   ├── student.ts             # Pinia: student state
│   │   │   ├── chat.ts                # Pinia: chat state
│   │   │   ├── dashboard.ts           # Pinia: dashboard state
│   │   │   └── notifications.ts       # Pinia: realtime notifications
│   │   │
│   │   ├── api/
│   │   │   ├── client.ts              # Axios instance + auth interceptor
│   │   │   ├── auth.ts                # Telegram auth API
│   │   │   ├── students.ts
│   │   │   ├── chat.ts
│   │   │   ├── lessons.ts
│   │   │   └── dashboard.ts
│   │   │
│   │   ├── components/
│   │   │   ├── layout/
│   │   │   │   ├── Header.vue
│   │   │   │   ├── Sidebar.vue
│   │   │   │   └── Footer.vue
│   │   │   │
│   │   │   ├── sections/
│   │   │   │   ├── ProblemSection.vue       # Section 1: Исходная проблема
│   │   │   │   ├── SolutionSection.vue      # Section 2: Решение + Timeline
│   │   │   │   ├── AiAssistantSection.vue   # Section 3: AI-ассистент (чат)
│   │   │   │   ├── StudentCabinetSection.vue# Section 4: Личный кабинет
│   │   │   │   ├── CuratorDashboardSection.vue # Section 5: Дашборд кураторов
│   │   │   │   ├── ResultsSection.vue       # Section 6: Результаты
│   │   │   │   └── FinancialSection.vue     # Section 7: Финансы
│   │   │   │
│   │   │   ├── chat/
│   │   │   │   ├── ChatWindow.vue           # Основной чат
│   │   │   │   ├── ChatMessage.vue          # Сообщение
│   │   │   │   ├── ChatInput.vue            # Поле ввода
│   │   │   │   └── TypingIndicator.vue      # "AI печатает..."
│   │   │   │
│   │   │   ├── student/
│   │   │   │   ├── StudentProfile.vue       # Профиль студента
│   │   │   │   ├── LessonList.vue           # Список уроков
│   │   │   │   ├── LessonCard.vue           # Карточка урока
│   │   │   │   ├── ProgressBar.vue          # Анимированный прогресс
│   │   │   │   ├── TestResults.vue          # Результаты тестов
│   │   │   │   └── Certificate.vue          # Сертификат (PDF download)
│   │   │   │
│   │   │   ├── dashboard/
│   │   │   │   ├── StudentTable.vue         # Таблица студентов
│   │   │   │   ├── StudentRow.vue           # Строка студента
│   │   │   │   ├── RiskBadge.vue            # Индикатор риска
│   │   │   │   ├── FilterBar.vue            # Фильтры
│   │   │   │   ├── NotificationPanel.vue    # Уведомления
│   │   │   │   └── MetricsCards.vue         # Карточки метрик
│   │   │   │
│   │   │   ├── charts/
│   │   │   │   ├── RetentionChart.vue       # Линейный график retention
│   │   │   │   ├── ProfitChart.vue          # Столбчатая диаграмма
│   │   │   │   ├── HoursSavedGauge.vue      # Gauge chart
│   │   │   │   └── ComparisonTable.vue      # До vs После
│   │   │   │
│   │   │   └── ui/
│   │   │       ├── AnimatedCounter.vue      # Анимированные числа
│   │   │       ├── TimelineItem.vue         # Элемент таймлайна
│   │   │       ├── MetricCard.vue           # Карточка метрики
│   │   │       ├── StatusBadge.vue          # Статус-бейдж
│   │   │       └── Toast.vue                # Toast-уведомления
│   │   │
│   │   ├── views/
│   │   │   └── CaseStudyView.vue            # Главная страница кейса
│   │   │
│   │   ├── composables/
│   │   │   ├── useTelegramAuth.ts           # Telegram Mini App auth
│   │   │   ├── useChat.ts                   # Логика чата
│   │   │   ├── useNotifications.ts          # Real-time уведомления
│   │   │   └── useAnimatedMetrics.ts        # Анимация метрик
│   │   │
│   │   ├── types/
│   │   │   ├── auth.ts
│   │   │   ├── student.ts
│   │   │   ├── lesson.ts
│   │   │   ├── chat.ts
│   │   │   └── metrics.ts
│   │   │
│   │   └── assets/
│   │       ├── styles/
│   │       │   └── main.css               # Tailwind imports
│   │       └── images/
│   │           ├── screenshots/           # Скриншоты "до"
│   │           └── icons/
│   │
│   ├── public/
│   │   └── certificate-template.pdf
│   │
│   ├── index.html
│   ├── vite.config.ts
│   ├── tailwind.config.js
│   ├── tsconfig.json
│   ├── package.json
│   ├── Dockerfile
│   └── .dockerignore
│
├── docker/
│   ├── docker-compose.yml             # Local development
│   ├── docker-compose.prod.yml        # Production reference
│   └── nginx/
│       └── nginx.conf
│
├── justfile                           # Task runner commands
├── .env.example
├── .gitignore
└── README.md
```

---

## 2. Модели данных (PostgreSQL)

> **Directus**: Используется как удобная админ-панель для просмотра и редактирования данных в БД.
> Подключается к той же PostgreSQL, автоматически генерирует UI для всех таблиц.

### 2.1 Основные сущности

```sql
-- Пользователи (Telegram auth)
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    telegram_id BIGINT UNIQUE NOT NULL,      -- Telegram User ID
    telegram_username VARCHAR(255),
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    photo_url VARCHAR(500),
    role VARCHAR(50) DEFAULT 'student',       -- student, curator, admin
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_users_telegram_id ON users(telegram_id);

-- Студенты (расширение user для демо-данных)
CREATE TABLE students (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),        -- Связь с telegram user (nullable для демо)
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255),
    avatar_url VARCHAR(500),
    enrolled_at TIMESTAMP DEFAULT NOW(),
    last_active_at TIMESTAMP,
    status VARCHAR(50) DEFAULT 'active', -- active, at_risk, dropped, completed
    risk_score INTEGER DEFAULT 0,        -- 0-100, выше = больше риск
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Курсы
CREATE TABLE courses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    total_lessons INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Уроки
CREATE TABLE lessons (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    course_id UUID REFERENCES courses(id),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    order_index INTEGER NOT NULL,
    content_type VARCHAR(50), -- video, text, quiz
    duration_minutes INTEGER,
    is_locked BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Прогресс студента
CREATE TABLE student_progress (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    student_id UUID REFERENCES students(id),
    course_id UUID REFERENCES courses(id),
    lesson_id UUID REFERENCES lessons(id),
    status VARCHAR(50) DEFAULT 'not_started', -- not_started, in_progress, completed
    progress_percent INTEGER DEFAULT 0,
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    UNIQUE(student_id, lesson_id)
);

-- Тесты
CREATE TABLE tests (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    lesson_id UUID REFERENCES lessons(id),
    title VARCHAR(255) NOT NULL,
    max_score INTEGER DEFAULT 100,
    passing_score INTEGER DEFAULT 70
);

-- Результаты тестов
CREATE TABLE test_results (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    student_id UUID REFERENCES students(id),
    test_id UUID REFERENCES tests(id),
    score INTEGER NOT NULL,
    passed BOOLEAN NOT NULL,
    completed_at TIMESTAMP DEFAULT NOW()
);

-- Домашние задания
CREATE TABLE homework (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    lesson_id UUID REFERENCES lessons(id),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    due_days INTEGER DEFAULT 7
);

-- Сданные домашки
CREATE TABLE homework_submissions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    student_id UUID REFERENCES students(id),
    homework_id UUID REFERENCES homework(id),
    content TEXT,
    file_url VARCHAR(500),
    status VARCHAR(50) DEFAULT 'pending', -- pending, ai_checked, curator_reviewed
    ai_score INTEGER,
    ai_feedback TEXT,
    curator_score INTEGER,
    curator_feedback TEXT,
    submitted_at TIMESTAMP DEFAULT NOW(),
    reviewed_at TIMESTAMP
);

-- Чат-сессии
CREATE TABLE chat_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    student_id UUID REFERENCES students(id),
    started_at TIMESTAMP DEFAULT NOW(),
    ended_at TIMESTAMP
);

-- Сообщения чата
CREATE TABLE chat_messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID REFERENCES chat_sessions(id),
    role VARCHAR(20) NOT NULL, -- user, assistant
    content TEXT NOT NULL,
    response_time_ms INTEGER,  -- время ответа AI
    resolved_by_ai BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Векторное хранилище (pgvector) для knowledge base
CREATE TABLE knowledge_embeddings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    content TEXT NOT NULL,
    embedding vector(1536),    -- OpenAI embeddings
    source_type VARCHAR(50),   -- lesson, faq, grammar_rule
    source_id UUID,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Уведомления
CREATE TABLE notifications (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    type VARCHAR(50) NOT NULL, -- homework_submitted, lesson_completed, student_at_risk
    title VARCHAR(255) NOT NULL,
    message TEXT,
    student_id UUID REFERENCES students(id),
    read BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Метрики (для демо)
CREATE TABLE daily_metrics (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    date DATE UNIQUE NOT NULL,
    total_students INTEGER,
    active_students INTEGER,
    completed_courses INTEGER,
    ai_questions_answered INTEGER,
    ai_resolution_rate DECIMAL(5,2),
    retention_rate DECIMAL(5,2),
    created_at TIMESTAMP DEFAULT NOW()
);
```

### 2.2 Индексы

```sql
CREATE INDEX idx_students_status ON students(status);
CREATE INDEX idx_students_risk ON students(risk_score DESC);
CREATE INDEX idx_progress_student ON student_progress(student_id);
CREATE INDEX idx_chat_session ON chat_messages(session_id);
CREATE INDEX idx_notifications_unread ON notifications(read) WHERE read = false;

-- pgvector index
CREATE INDEX idx_embeddings ON knowledge_embeddings 
USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);
```

---

## 3. API Endpoints (FastAPI)

### 3.0 Auth API (Telegram)

```
POST   /api/auth/telegram               # Авторизация через Telegram initData
       Request:  { "init_data": "query_string_from_telegram" }
       Response: { "access_token": "jwt...", "user": {...} }

GET    /api/auth/me                     # Текущий пользователь (требует JWT)
       Response: { "id": "uuid", "telegram_id": 123456, "role": "student" }

POST   /api/auth/logout                 # Выход (инвалидация токена в Redis)
```

### 3.1 Students API

```
GET    /api/students                    # Список студентов (с фильтрами)
GET    /api/students/{id}               # Детали студента
GET    /api/students/{id}/progress      # Прогресс студента
GET    /api/students/{id}/tests         # Результаты тестов
POST   /api/students/{id}/complete-lesson  # Завершить урок (demo)
```

### 3.2 Lessons API

```
GET    /api/courses                     # Список курсов
GET    /api/courses/{id}/lessons        # Уроки курса
GET    /api/lessons/{id}                # Детали урока
```

### 3.3 Homework API

```
GET    /api/homework/{student_id}       # ДЗ студента
POST   /api/homework/{id}/submit        # Сдать ДЗ
GET    /api/homework/{id}/result        # Результат проверки
```

### 3.4 Chat API (AI Assistant)

```
POST   /api/chat/message                # Отправить вопрос AI
GET    /api/chat/history/{student_id}   # История чата
GET    /api/chat/stats                  # Статистика AI (% resolved)
```

### 3.5 Dashboard API

```
GET    /api/dashboard/students          # Студенты с рисками
GET    /api/dashboard/notifications     # Уведомления куратора
GET    /api/dashboard/metrics           # Метрики в реальном времени
POST   /api/dashboard/notifications/{id}/read  # Пометить прочитанным
```

### 3.6 Metrics API

```
GET    /api/metrics/retention           # Данные retention (для графика)
GET    /api/metrics/profit              # Данные прибыли
GET    /api/metrics/comparison          # До vs После
GET    /api/metrics/summary             # Общая сводка
```

---

## 4. Vue Router

```typescript
const routes = [
  {
    path: '/',
    component: CaseStudyView,
    children: [
      { path: '', redirect: '/problem' },
      { path: 'problem', component: ProblemSection },
      { path: 'solution', component: SolutionSection },
      { path: 'ai-assistant', component: AiAssistantSection },
      { path: 'student-cabinet', component: StudentCabinetSection },
      { path: 'dashboard', component: CuratorDashboardSection },
      { path: 'results', component: ResultsSection },
      { path: 'financial', component: FinancialSection },
    ]
  }
]
```

**Альтернатива**: Single-page scroll с навигацией по секциям (anchor links).

---

## 5. Интеграции

### 5.0 Telegram Auth (python-jose + httpx)

```python
# services/auth_service.py
import hmac
import hashlib
from urllib.parse import parse_qsl
from datetime import datetime, timedelta
from jose import jwt
from app.config import settings

class TelegramAuthService:
    """Валидация Telegram Mini App initData и генерация JWT"""
    
    def validate_init_data(self, init_data: str) -> dict | None:
        """
        Валидирует initData от Telegram Mini App.
        https://core.telegram.org/bots/webapps#validating-data-received-via-the-mini-app
        """
        # Парсим query string
        parsed = dict(parse_qsl(init_data, keep_blank_values=True))
        
        # Извлекаем hash
        received_hash = parsed.pop('hash', None)
        if not received_hash:
            return None
        
        # Сортируем и формируем data-check-string
        data_check_string = '\n'.join(
            f"{k}={v}" for k, v in sorted(parsed.items())
        )
        
        # Вычисляем secret_key = HMAC-SHA256(bot_token, "WebAppData")
        secret_key = hmac.new(
            b"WebAppData",
            settings.TELEGRAM_BOT_TOKEN.encode(),
            hashlib.sha256
        ).digest()
        
        # Вычисляем hash
        computed_hash = hmac.new(
            secret_key,
            data_check_string.encode(),
            hashlib.sha256
        ).hexdigest()
        
        # Сравниваем
        if not hmac.compare_digest(computed_hash, received_hash):
            return None
        
        # Проверяем auth_date (не старше 24 часов)
        auth_date = int(parsed.get('auth_date', 0))
        if datetime.now().timestamp() - auth_date > 86400:
            return None
        
        # Парсим user data
        import json
        user_data = json.loads(parsed.get('user', '{}'))
        return user_data
    
    def create_access_token(self, telegram_id: int, role: str = "student") -> str:
        """Создает JWT токен"""
        expire = datetime.utcnow() + timedelta(minutes=settings.JWT_EXPIRE_MINUTES)
        payload = {
            "sub": str(telegram_id),
            "role": role,
            "exp": expire
        }
        return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    
    def verify_token(self, token: str) -> dict | None:
        """Верифицирует JWT токен"""
        try:
            payload = jwt.decode(
                token, 
                settings.JWT_SECRET, 
                algorithms=[settings.JWT_ALGORITHM]
            )
            return payload
        except jwt.JWTError:
            return None
```

```python
# api/auth.py
from fastapi import APIRouter, HTTPException, Depends
from app.services.auth_service import TelegramAuthService
from app.schemas.auth import TelegramAuthRequest, TokenResponse
from app.db.session import get_db
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["auth"])
auth_service = TelegramAuthService()

@router.post("/telegram", response_model=TokenResponse)
async def telegram_auth(request: TelegramAuthRequest, db = Depends(get_db)):
    """Авторизация через Telegram Mini App"""
    
    # Валидируем initData
    user_data = auth_service.validate_init_data(request.init_data)
    if not user_data:
        raise HTTPException(status_code=401, detail="Invalid Telegram auth data")
    
    telegram_id = user_data.get("id")
    
    # Ищем или создаем пользователя
    user = await db.get(User, User.telegram_id == telegram_id)
    if not user:
        user = User(
            telegram_id=telegram_id,
            telegram_username=user_data.get("username"),
            first_name=user_data.get("first_name"),
            last_name=user_data.get("last_name"),
            photo_url=user_data.get("photo_url"),
        )
        db.add(user)
        await db.commit()
    
    # Генерируем токен
    token = auth_service.create_access_token(telegram_id, user.role)
    
    return TokenResponse(access_token=token, user=user)
```

```typescript
// frontend/src/composables/useTelegramAuth.ts
import WebApp from '@twa-dev/sdk'
import { ref, onMounted } from 'vue'
import { authApi } from '@/api/auth'
import { useAuthStore } from '@/stores/auth'

export function useTelegramAuth() {
  const authStore = useAuthStore()
  const isLoading = ref(true)
  const error = ref<string | null>(null)

  onMounted(async () => {
    try {
      // Получаем initData из Telegram Mini App SDK
      const initData = WebApp.initData
      
      if (!initData) {
        // Для dev режима без Telegram
        if (import.meta.env.DEV) {
          console.warn('No Telegram initData, using demo mode')
          authStore.setDemoMode()
          return
        }
        throw new Error('Telegram initData not available')
      }
      
      // Отправляем на бэкенд для валидации
      const response = await authApi.telegramAuth(initData)
      
      // Сохраняем токен и user
      authStore.setAuth(response.access_token, response.user)
      
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'Auth failed'
    } finally {
      isLoading.value = false
    }
  })

  return { isLoading, error }
}
```

### 5.1 AI Assistant (OpenAI)

```python
# services/ai_assistant.py

class AIAssistant:
    """AI-ассистент для ответов на вопросы студентов"""
    
    async def answer(self, question: str, student_id: UUID) -> AIResponse:
        # 1. Поиск релевантного контекста в knowledge base (pgvector)
        context = await self.search_knowledge(question)
        
        # 2. Формирование промпта
        prompt = self.build_prompt(question, context)
        
        # 3. Запрос к OpenAI
        response = await self.openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ]
        )
        
        # 4. Сохранение в историю
        await self.save_message(student_id, question, response)
        
        return AIResponse(
            answer=response.choices[0].message.content,
            response_time_ms=elapsed_ms,
            sources=context.sources
        )
```

### 5.2 GetCourse Integration (Mock for Demo)

```python
# integrations/getcourse.py

class GetCourseClient:
    """Mock клиент GetCourse для демонстрации"""
    
    async def sync_students(self) -> list[Student]:
        """Синхронизация студентов из GetCourse"""
        pass
    
    async def get_course_progress(self, student_id: str) -> Progress:
        """Получение прогресса из GetCourse"""
        pass
    
    async def send_notification(self, student_id: str, message: str):
        """Отправка уведомления через GetCourse"""
        pass
```

### 5.3 Real-time Notifications (WebSocket)

```python
# api/websocket.py

@router.websocket("/ws/notifications")
async def notifications_websocket(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Получаем новые события и отправляем клиенту
            notification = await notification_queue.get()
            await websocket.send_json(notification.dict())
    except WebSocketDisconnect:
        manager.disconnect(websocket)
```

---

## 6. Демо-данные

### 6.1 Студенты (seed)

```python
DEMO_STUDENTS = [
    {
        "name": "Александр Петров",
        "status": "active",
        "progress": 65,
        "risk_score": 10,
        "course": "Английский для бизнеса"
    },
    {
        "name": "Иван Иванов", 
        "status": "at_risk",
        "progress": 40,
        "risk_score": 75,
        "last_homework_days_ago": 3
    },
    {
        "name": "Мария Сидорова",
        "status": "at_risk", 
        "progress": 35,
        "risk_score": 60,
        "lessons_behind": 2
    },
    {
        "name": "Елена Морозова",
        "status": "active",
        "progress": 55,
        "risk_score": 5
    },
    # ... ещё ~15 студентов для демо
]
```

### 6.2 Вопросы AI (предзаготовленные ответы)

```python
DEMO_QA = [
    {
        "question": "Как правильно произнести слово 'schedule'?",
        "answer": "В британском английском: /ˈʃedjuːl/ (шедьюл)\nВ американском: /ˈskedʒuːl/ (скеджул)\n\nОба варианта правильные!"
    },
    {
        "question": "Я не понимаю Present Perfect",
        "answer": "Present Perfect используется когда:\n\n1. **Действие началось в прошлом и продолжается сейчас**\n   - I have lived here for 5 years.\n\n2. **Результат действия важен сейчас**\n   - I have lost my keys (= я их ищу)\n\n3. **Опыт в жизни**\n   - Have you ever been to London?\n\n**Формула**: have/has + V3 (past participle)"
    },
    # ... ещё 10-15 типовых вопросов
]
```

---

## 7. Интерактивные фичи (реализация)

### 7.1 Работающий чат с AI

```vue
<!-- components/chat/ChatWindow.vue -->
<template>
  <div class="chat-container">
    <div class="messages" ref="messagesRef">
      <ChatMessage 
        v-for="msg in messages" 
        :key="msg.id"
        :message="msg"
      />
      <TypingIndicator v-if="isTyping" />
    </div>
    <ChatInput @send="handleSend" :disabled="isTyping" />
  </div>
</template>

<script setup lang="ts">
const handleSend = async (text: string) => {
  // 1. Добавляем сообщение пользователя
  addMessage({ role: 'user', content: text })
  
  // 2. Показываем индикатор
  isTyping.value = true
  
  // 3. Запрос к API
  const startTime = Date.now()
  const response = await chatApi.sendMessage(text)
  const elapsed = Date.now() - startTime
  
  // 4. Добавляем ответ AI
  isTyping.value = false
  addMessage({ 
    role: 'assistant', 
    content: response.answer,
    responseTime: elapsed
  })
}
</script>
```

### 7.2 Фильтр по статусу студентов

```vue
<!-- components/dashboard/FilterBar.vue -->
<template>
  <div class="flex gap-2">
    <button 
      v-for="filter in filters"
      :key="filter.value"
      :class="[
        'px-4 py-2 rounded-lg transition',
        activeFilter === filter.value 
          ? 'bg-blue-600 text-white' 
          : 'bg-gray-100 hover:bg-gray-200'
      ]"
      @click="setFilter(filter.value)"
    >
      <span :class="filter.dotClass" />
      {{ filter.label }}
      <span class="ml-1 text-sm">({{ filter.count }})</span>
    </button>
  </div>
</template>
```

### 7.3 Real-time уведомления

```typescript
// composables/useNotifications.ts
export function useNotifications() {
  const notifications = ref<Notification[]>([])
  
  onMounted(() => {
    // WebSocket для real-time
    const ws = new WebSocket(`${WS_URL}/ws/notifications`)
    
    ws.onmessage = (event) => {
      const notification = JSON.parse(event.data)
      notifications.value.unshift(notification)
      
      // Toast уведомление
      showToast(notification)
    }
  })
  
  return { notifications }
}
```

### 7.4 Анимированные графики

```vue
<!-- components/charts/RetentionChart.vue -->
<template>
  <div class="chart-container">
    <canvas ref="chartRef"></canvas>
  </div>
</template>

<script setup lang="ts">
import { Chart } from 'chart.js'

onMounted(() => {
  const ctx = chartRef.value.getContext('2d')
  
  new Chart(ctx, {
    type: 'line',
    data: {
      labels: ['Янв', 'Фев', 'Мар', 'Апр', 'Май', 'Июн'],
      datasets: [
        {
          label: 'До внедрения',
          data: [85, 84, 83, 85, 84, 85],
          borderColor: '#ef4444',
          tension: 0.4
        },
        {
          label: 'После внедрения',
          data: [85, 87, 89, 90, 91, 92],
          borderColor: '#22c55e',
          tension: 0.4
        }
      ]
    },
    options: {
      animation: {
        duration: 2000,
        easing: 'easeOutQuart'
      }
    }
  })
})
</script>
```

---

## 8. Docker & Coolify Deploy

### 8.1 Backend Dockerfile

```dockerfile
# backend/Dockerfile
FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY pyproject.toml ./
RUN pip install --no-cache-dir -e .

# Copy application
COPY app ./app

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

# Granian ASGI server
CMD ["granian", "--interface", "asgi", "--host", "0.0.0.0", "--port", "8000", "app.main:app"]
```

### 8.2 Frontend Dockerfile

```dockerfile
# frontend/Dockerfile
FROM node:20-alpine AS builder

WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### 8.3 Docker Compose (Local Development)

```yaml
# docker/docker-compose.yml
services:
  backend:
    build: ../backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql+asyncpg://postgres:postgres@db:5432/education
      - REDIS_URL=redis://redis:6379
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - TELEGRAM_BOT_TOKEN=${TELEGRAM_BOT_TOKEN}
      - JWT_SECRET=${JWT_SECRET}
      - MINIO_ENDPOINT=minio:9000
      - MINIO_ACCESS_KEY=${MINIO_ACCESS_KEY}
      - MINIO_SECRET_KEY=${MINIO_SECRET_KEY}
    depends_on:
      - db
      - redis
    volumes:
      - ../backend/app:/app/app  # Hot reload

  frontend:
    build: ../frontend
    ports:
      - "3000:80"
    depends_on:
      - backend

  db:
    image: pgvector/pgvector:pg16
    environment:
      POSTGRES_DB: education
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

  directus:
    image: directus/directus:11
    ports:
      - "8055:8055"
    environment:
      SECRET: ${DIRECTUS_SECRET}
      ADMIN_EMAIL: admin@example.com
      ADMIN_PASSWORD: ${DIRECTUS_ADMIN_PASSWORD}
      DB_CLIENT: pg
      DB_HOST: db
      DB_PORT: 5432
      DB_DATABASE: education
      DB_USER: postgres
      DB_PASSWORD: postgres
      WEBSOCKETS_ENABLED: "true"
    depends_on:
      - db

  minio:
    image: minio/minio
    ports:
      - "9000:9000"
      - "9001:9001"
    environment:
      MINIO_ROOT_USER: ${MINIO_ACCESS_KEY}
      MINIO_ROOT_PASSWORD: ${MINIO_SECRET_KEY}
    volumes:
      - minio_data:/data
    command: server /data --console-address ":9001"

volumes:
  postgres_data:
  redis_data:
  minio_data:
```

### 8.4 Coolify Deployment

В Coolify создаём следующие сервисы:

**1. Backend**
- Source: GitHub repo
- Build: Dockerfile (backend/Dockerfile)
- Port: 8000
- Health check: `/health`

**2. Frontend**
- Source: GitHub repo  
- Build: Dockerfile (frontend/Dockerfile)
- Port: 80
- Domain: education.yourdomain.com

**3. PostgreSQL**
- Image: `pgvector/pgvector:pg16`
- Persistent volume for data

**4. Redis**
- Image: `redis:7-alpine`
- Persistent volume

**5. Directus**
- Image: `directus/directus:11`
- Connect to same PostgreSQL
- Port: 8055 (internal access)

**6. MinIO**
- Image: `minio/minio`
- Persistent volume
- Ports: 9000 (API), 9001 (Console)

### 8.5 Environment Variables (.env.example)

```env
# Database
DATABASE_URL=postgresql+asyncpg://postgres:postgres@db:5432/education

# Redis
REDIS_URL=redis://redis:6379

# JWT
JWT_SECRET=your-super-secret-key-change-in-production
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=10080  # 7 days

# Telegram
TELEGRAM_BOT_TOKEN=123456:ABC-your-bot-token

# OpenAI
OPENAI_API_KEY=sk-your-openai-key

# MinIO / S3
MINIO_ENDPOINT=minio:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin
MINIO_BUCKET=education

# Directus
DIRECTUS_SECRET=your-directus-secret
DIRECTUS_ADMIN_PASSWORD=admin123

# App
DEBUG=true
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
```

---

## 9. Justfile (Task Runner)

```just
# justfile

# ==================== Development ====================

# Run backend with hot reload
dev-backend:
    cd backend && granian --interface asgi --reload app.main:app

# Run frontend dev server
dev-frontend:
    cd frontend && npm run dev

# Run both in parallel
dev:
    just dev-backend &
    just dev-frontend

# ==================== Database ====================

# Run migrations
db-migrate:
    cd backend && alembic upgrade head

# Create new migration
db-migration name:
    cd backend && alembic revision --autogenerate -m "{{name}}"

# Seed demo data
db-seed:
    cd backend && python -m app.db.seed

# Reset database (drop + create + migrate + seed)
db-reset:
    docker-compose -f docker/docker-compose.yml down -v
    docker-compose -f docker/docker-compose.yml up -d db
    sleep 3
    just db-migrate
    just db-seed

# ==================== Docker ====================

# Start all services
up:
    docker-compose -f docker/docker-compose.yml up -d

# Stop all services
down:
    docker-compose -f docker/docker-compose.yml down

# View logs
logs service="":
    docker-compose -f docker/docker-compose.yml logs -f {{service}}

# Rebuild and restart
rebuild service:
    docker-compose -f docker/docker-compose.yml up -d --build {{service}}

# ==================== Testing & Linting ====================

# Run all tests
test:
    cd backend && pytest -v

# Run tests with coverage
test-cov:
    cd backend && pytest --cov=app --cov-report=html

# Lint backend
lint-backend:
    cd backend && ruff check . && mypy app

# Lint frontend
lint-frontend:
    cd frontend && npm run lint && npm run type-check

# Lint all
lint:
    just lint-backend
    just lint-frontend

# Format code
fmt:
    cd backend && ruff format .
    cd frontend && npm run format

# ==================== Build ====================

# Build Docker images
build:
    docker-compose -f docker/docker-compose.yml build

# Build frontend for production
build-frontend:
    cd frontend && npm run build

# ==================== Utilities ====================

# Open Directus admin panel
directus:
    xdg-open http://localhost:8055 || open http://localhost:8055

# Open MinIO console
minio:
    xdg-open http://localhost:9001 || open http://localhost:9001

# Generate OpenAPI schema
openapi:
    cd backend && python -c "from app.main import app; import json; print(json.dumps(app.openapi(), indent=2))" > openapi.json
```

---

## 10. Этапы разработки

### Phase 1: Базовая инфраструктура (2-3 дня)
- [ ] Настройка FastAPI проекта
- [ ] Настройка Vue + Vite + Tailwind
- [ ] Docker Compose с PostgreSQL + Redis
- [ ] Базовые модели и миграции

### Phase 2: Backend API (3-4 дня)
- [ ] Students API + CRUD
- [ ] Lessons/Courses API
- [ ] Homework API с AI проверкой
- [ ] Chat API с OpenAI интеграцией
- [ ] Dashboard API
- [ ] Metrics API
- [ ] WebSocket для real-time

### Phase 3: Frontend Sections (4-5 дней)
- [ ] Layout (Header, навигация)
- [ ] Section 1: Problem (статика + скриншоты)
- [ ] Section 2: Solution + Timeline
- [ ] Section 3: AI Assistant (интерактивный чат)
- [ ] Section 4: Student Cabinet (интерактив)
- [ ] Section 5: Curator Dashboard (фильтры, уведомления)
- [ ] Section 6: Results (анимированные графики)
- [ ] Section 7: Financial Summary

### Phase 4: Интерактив + Polish (2-3 дня)
- [ ] WebSocket уведомления
- [ ] Анимации (графики, прогресс-бары)
- [ ] Демо-данные + сидинг
- [ ] Тестирование
- [ ] Responsive дизайн

### Phase 5: Deploy (1 день)
- [ ] Push to GitHub
- [ ] Configure Coolify services
- [ ] Set environment variables in Coolify
- [ ] Configure domains & SSL (auto via Coolify)
- [ ] Verify Directus connection to DB

---

## 11. Ключевые метрики для демо

| Метрика | До | После | Изменение |
|---------|-----|-------|-----------|
| Retention | 85% | 92% | +7% |
| Студентов/месяц | 0 | +45 | +45 |
| Кураторов | 3 | 1 | -2 |
| Часов на поддержку | 60/нед | 15/нед | -75% |
| Время ответа | 2-4 часа | 2-3 сек | -99.9% |
| AI resolution rate | 0% | 90% | +90% |
| Прибыль/месяц | базовая | +370к ₽ | - |
| ROI | - | 30 дней | - |

# Database Schema

## ER Diagram (текстовое описание)

```
┌─────────────┐       ┌─────────────┐
│   users     │       │   courses   │
├─────────────┤       ├─────────────┤
│ id (PK)     │       │ id (PK)     │
│ telegram_id │       │ title       │
│ username    │       │ description │
│ first_name  │       │ total_lessons│
│ last_name   │       └──────┬──────┘
│ photo_url   │              │
│ role        │              │ 1:N
│ is_active   │              │
└──────┬──────┘       ┌──────▼──────┐
       │              │   lessons   │
       │ 1:1          ├─────────────┤
       │              │ id (PK)     │
┌──────▼──────┐       │ course_id(FK)│
│  students   │       │ title       │
├─────────────┤       │ order_index │
│ id (PK)     │       │ content_type│
│ user_id(FK) │       │ duration    │
│ name        │       │ is_locked   │
│ email       │       └──────┬──────┘
│ status      │              │
│ risk_score  │              │ 1:N
│ enrolled_at │              │
│ last_active │       ┌──────┼──────────────┐
└──────┬──────┘       │      │              │
       │              │      │              │
       │         ┌────▼───┐ ┌▼────────┐ ┌───▼────┐
       │         │ tests  │ │homework │ │progress│
       │         └────┬───┘ └────┬────┘ └───┬────┘
       │              │          │          │
       │              │          │          │
       │         ┌────▼─────┐ ┌──▼─────────┐│
       └────────►│test_results│ │submissions ││
                 └───────────┘ └────────────┘│
       │                                     │
       └─────────────────────────────────────┘
       │
       │         ┌─────────────┐
       │         │chat_sessions│
       └────────►├─────────────┤
                 │ id (PK)     │
                 │ student_id  │
                 │ started_at  │
                 └──────┬──────┘
                        │ 1:N
                 ┌──────▼──────┐
                 │chat_messages│
                 ├─────────────┤
                 │ id (PK)     │
                 │ session_id  │
                 │ role        │
                 │ content     │
                 │ response_ms │
                 └─────────────┘
```

## Tables

### users
Пользователи системы (авторизация через Telegram)

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK | Уникальный идентификатор |
| telegram_id | BIGINT | UNIQUE, NOT NULL, INDEX | Telegram User ID |
| telegram_username | VARCHAR(255) | | Username в Telegram |
| first_name | VARCHAR(255) | | Имя |
| last_name | VARCHAR(255) | | Фамилия |
| photo_url | VARCHAR(500) | | URL аватара |
| role | VARCHAR(50) | DEFAULT 'student' | student / curator / admin |
| is_active | BOOLEAN | DEFAULT true | Активен ли аккаунт |
| created_at | TIMESTAMPTZ | DEFAULT now() | |
| updated_at | TIMESTAMPTZ | DEFAULT now() | |

### students
Профили студентов (могут быть связаны с user или быть демо-данными)

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK | |
| user_id | UUID | FK → users.id, NULLABLE | Связь с Telegram-аккаунтом |
| name | VARCHAR(255) | NOT NULL | ФИО студента |
| email | VARCHAR(255) | | Email |
| avatar_url | VARCHAR(500) | | Аватар |
| enrolled_at | TIMESTAMPTZ | DEFAULT now() | Дата записи на курс |
| last_active_at | TIMESTAMPTZ | | Последняя активность |
| status | VARCHAR(50) | DEFAULT 'active' | active / at_risk / dropped / completed |
| risk_score | INTEGER | DEFAULT 0 | 0-100, выше = больше риск отвала |
| created_at | TIMESTAMPTZ | | |
| updated_at | TIMESTAMPTZ | | |

**Indexes**: status, risk_score DESC

### courses
Курсы

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK | |
| title | VARCHAR(255) | NOT NULL | Название курса |
| description | TEXT | | Описание |
| total_lessons | INTEGER | NOT NULL | Общее количество уроков |
| created_at | TIMESTAMPTZ | | |
| updated_at | TIMESTAMPTZ | | |

### lessons
Уроки внутри курса

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK | |
| course_id | UUID | FK → courses.id, NOT NULL | |
| title | VARCHAR(255) | NOT NULL | Название урока |
| description | TEXT | | Описание |
| order_index | INTEGER | NOT NULL | Порядковый номер |
| content_type | VARCHAR(50) | | video / text / quiz |
| duration_minutes | INTEGER | | Длительность в минутах |
| is_locked | BOOLEAN | DEFAULT false | Заблокирован до прохождения предыдущего |
| created_at | TIMESTAMPTZ | | |
| updated_at | TIMESTAMPTZ | | |

### student_progress
Прогресс студента по урокам

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK | |
| student_id | UUID | FK → students.id, NOT NULL, INDEX | |
| course_id | UUID | FK → courses.id, NOT NULL | |
| lesson_id | UUID | FK → lessons.id, NOT NULL | |
| status | VARCHAR(50) | DEFAULT 'not_started' | not_started / in_progress / completed |
| progress_percent | INTEGER | DEFAULT 0 | 0-100 |
| started_at | TIMESTAMPTZ | | |
| completed_at | TIMESTAMPTZ | | |

**Constraints**: UNIQUE(student_id, lesson_id)

### tests
Тесты к урокам

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK | |
| lesson_id | UUID | FK → lessons.id, NOT NULL | |
| title | VARCHAR(255) | NOT NULL | |
| max_score | INTEGER | DEFAULT 100 | Максимальный балл |
| passing_score | INTEGER | DEFAULT 70 | Проходной балл |
| created_at | TIMESTAMPTZ | | |
| updated_at | TIMESTAMPTZ | | |

### test_results
Результаты тестов

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK | |
| student_id | UUID | FK → students.id, NOT NULL | |
| test_id | UUID | FK → tests.id, NOT NULL | |
| score | INTEGER | NOT NULL | Набранный балл |
| passed | BOOLEAN | NOT NULL | Сдан ли тест |
| completed_at | TIMESTAMPTZ | DEFAULT now() | |

### homework
Домашние задания

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK | |
| lesson_id | UUID | FK → lessons.id, NOT NULL | |
| title | VARCHAR(255) | NOT NULL | |
| description | TEXT | | Описание задания |
| due_days | INTEGER | DEFAULT 7 | Дней на выполнение |
| created_at | TIMESTAMPTZ | | |
| updated_at | TIMESTAMPTZ | | |

### homework_submissions
Сданные домашние задания

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK | |
| student_id | UUID | FK → students.id, NOT NULL | |
| homework_id | UUID | FK → homework.id, NOT NULL | |
| content | TEXT | | Текст ответа |
| file_url | VARCHAR(500) | | URL файла (MinIO) |
| status | VARCHAR(50) | DEFAULT 'pending' | pending / ai_checked / curator_reviewed |
| ai_score | INTEGER | | Оценка AI |
| ai_feedback | TEXT | | Комментарий AI |
| curator_score | INTEGER | | Оценка куратора |
| curator_feedback | TEXT | | Комментарий куратора |
| submitted_at | TIMESTAMPTZ | DEFAULT now() | |
| reviewed_at | TIMESTAMPTZ | | |

### chat_sessions
Сессии чата с AI

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK | |
| student_id | UUID | FK → students.id, NOT NULL | |
| started_at | TIMESTAMPTZ | DEFAULT now() | |
| ended_at | TIMESTAMPTZ | | |

### chat_messages
Сообщения в чате

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK | |
| session_id | UUID | FK → chat_sessions.id, NOT NULL, INDEX | |
| role | VARCHAR(20) | NOT NULL | user / assistant |
| content | TEXT | NOT NULL | Текст сообщения |
| response_time_ms | INTEGER | | Время ответа AI в мс |
| resolved_by_ai | BOOLEAN | DEFAULT true | Решено ли AI |
| created_at | TIMESTAMPTZ | | |
| updated_at | TIMESTAMPTZ | | |

### knowledge_embeddings
Векторная база знаний для AI (pgvector)

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK | |
| content | TEXT | NOT NULL | Текст для поиска |
| embedding | FLOAT[] | | Вектор (1536 dims для OpenAI) |
| source_type | VARCHAR(50) | | lesson / faq / grammar_rule |
| source_id | UUID | | ID источника |
| created_at | TIMESTAMPTZ | | |
| updated_at | TIMESTAMPTZ | | |

### notifications
Уведомления для кураторов

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK | |
| type | VARCHAR(50) | NOT NULL | homework_submitted / lesson_completed / student_at_risk / test_passed / course_completed |
| title | VARCHAR(255) | NOT NULL | |
| message | TEXT | | |
| student_id | UUID | FK → students.id | |
| read | BOOLEAN | DEFAULT false, INDEX | Прочитано ли |
| created_at | TIMESTAMPTZ | | |
| updated_at | TIMESTAMPTZ | | |

### daily_metrics
Ежедневные метрики для графиков

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK | |
| date | DATE | UNIQUE, NOT NULL | |
| total_students | INTEGER | | Всего студентов |
| active_students | INTEGER | | Активных сегодня |
| completed_courses | INTEGER | | Завершили курс |
| ai_questions_answered | INTEGER | | Вопросов обработано AI |
| ai_resolution_rate | NUMERIC(5,2) | | % решенных AI |
| retention_rate | NUMERIC(5,2) | | % retention |
| created_at | TIMESTAMPTZ | | |
| updated_at | TIMESTAMPTZ | | |

## Enums

### UserRole
- `student` — студент
- `curator` — куратор
- `admin` — администратор

### StudentStatus
- `active` — активный студент
- `at_risk` — в зоне риска отвала
- `dropped` — отвалился
- `completed` — завершил курс

### ProgressStatus
- `not_started` — не начат
- `in_progress` — в процессе
- `completed` — завершен

### ContentType
- `video` — видео-урок
- `text` — текстовый материал
- `quiz` — тест/квиз

### SubmissionStatus
- `pending` — ожидает проверки
- `ai_checked` — проверено AI
- `curator_reviewed` — проверено куратором

### MessageRole
- `user` — сообщение студента
- `assistant` — ответ AI

### NotificationType
- `homework_submitted` — сдано ДЗ
- `lesson_completed` — урок завершен
- `student_at_risk` — студент в зоне риска
- `test_passed` — тест сдан
- `course_completed` — курс завершен

## Extensions

- **pgvector** — для векторного поиска в knowledge_embeddings

import asyncio
import uuid
from datetime import datetime, timedelta, timezone

from sqlalchemy import select

from app.db.session import async_session_factory
from app.models import (
    Course,
    Lesson,
    Test,
    Student,
    StudentProgress,
    TestResult,
    Homework,
    HomeworkSubmission,
    ChatSession,
    ChatMessage,
    Notification,
    DailyMetrics,
)
from app.models.student import StudentStatus, ProgressStatus
from app.models.course import ContentType
from app.models.homework import SubmissionStatus
from app.models.chat import MessageRole
from app.models.notification import NotificationType


COURSE_DATA = {
    "title": "Английский для бизнеса",
    "description": "Комплексный курс делового английского для профессионалов",
    "total_lessons": 8,
}

LESSONS_DATA = [
    {"title": "Введение в деловой английский", "content_type": ContentType.VIDEO, "duration_minutes": 30},
    {"title": "Базовая грамматика", "content_type": ContentType.TEXT, "duration_minutes": 45},
    {"title": "Аудирование: деловые переговоры", "content_type": ContentType.VIDEO, "duration_minutes": 40},
    {"title": "Разговорная практика", "content_type": ContentType.VIDEO, "duration_minutes": 50},
    {"title": "Деловая переписка", "content_type": ContentType.TEXT, "duration_minutes": 35},
    {"title": "Презентации на английском", "content_type": ContentType.VIDEO, "duration_minutes": 45},
    {"title": "Телефонные переговоры", "content_type": ContentType.VIDEO, "duration_minutes": 40},
    {"title": "Финальный проект", "content_type": ContentType.QUIZ, "duration_minutes": 60},
]

STUDENTS_DATA = [
    {"name": "Александр Петров", "email": "alex@example.com", "status": StudentStatus.ACTIVE, "risk_score": 10, "progress_pct": 65},
    {"name": "Иван Иванов", "email": "ivan@example.com", "status": StudentStatus.AT_RISK, "risk_score": 75, "progress_pct": 40},
    {"name": "Мария Сидорова", "email": "maria@example.com", "status": StudentStatus.AT_RISK, "risk_score": 60, "progress_pct": 35},
    {"name": "Елена Морозова", "email": "elena@example.com", "status": StudentStatus.ACTIVE, "risk_score": 5, "progress_pct": 55},
    {"name": "Дмитрий Козлов", "email": "dmitry@example.com", "status": StudentStatus.ACTIVE, "risk_score": 15, "progress_pct": 70},
    {"name": "Анна Новикова", "email": "anna@example.com", "status": StudentStatus.ACTIVE, "risk_score": 8, "progress_pct": 80},
    {"name": "Сергей Волков", "email": "sergey@example.com", "status": StudentStatus.COMPLETED, "risk_score": 0, "progress_pct": 100},
    {"name": "Ольга Соколова", "email": "olga@example.com", "status": StudentStatus.ACTIVE, "risk_score": 20, "progress_pct": 50},
    {"name": "Николай Федоров", "email": "nikolay@example.com", "status": StudentStatus.DROPPED, "risk_score": 90, "progress_pct": 25},
    {"name": "Татьяна Михайлова", "email": "tatiana@example.com", "status": StudentStatus.ACTIVE, "risk_score": 12, "progress_pct": 60},
    {"name": "Андрей Белов", "email": "andrey@example.com", "status": StudentStatus.ACTIVE, "risk_score": 5, "progress_pct": 75},
    {"name": "Екатерина Орлова", "email": "kate@example.com", "status": StudentStatus.AT_RISK, "risk_score": 55, "progress_pct": 30},
    {"name": "Павел Кузнецов", "email": "pavel@example.com", "status": StudentStatus.ACTIVE, "risk_score": 18, "progress_pct": 45},
    {"name": "Наталья Попова", "email": "natalia@example.com", "status": StudentStatus.COMPLETED, "risk_score": 0, "progress_pct": 100},
    {"name": "Виктор Лебедев", "email": "victor@example.com", "status": StudentStatus.ACTIVE, "risk_score": 25, "progress_pct": 55},
]

DEMO_CHAT = [
    {"role": MessageRole.USER, "content": "Как правильно произнести слово 'schedule'?"},
    {"role": MessageRole.ASSISTANT, "content": "В британском английском: /ˈʃedjuːl/ (шедьюл)\nВ американском: /ˈskedʒuːl/ (скеджул)\n\nОба варианта правильные!", "response_time_ms": 1850},
    {"role": MessageRole.USER, "content": "Я не понимаю Present Perfect"},
    {"role": MessageRole.ASSISTANT, "content": "Present Perfect используется когда:\n\n1. Действие началось в прошлом и продолжается сейчас\n   - I have lived here for 5 years.\n\n2. Результат действия важен сейчас\n   - I have lost my keys (= я их ищу)\n\n3. Опыт в жизни\n   - Have you ever been to London?\n\nФормула: have/has + V3 (past participle)", "response_time_ms": 2340},
]


async def seed_database() -> None:
    async with async_session_factory() as session:
        existing = await session.execute(select(Course).limit(1))
        if existing.scalar_one_or_none():
            print("Database already seeded, skipping...")
            return

        course = Course(
            id=uuid.uuid4(),
            title=COURSE_DATA["title"],
            description=COURSE_DATA["description"],
            total_lessons=COURSE_DATA["total_lessons"],
        )
        session.add(course)
        await session.flush()

        lessons: list[Lesson] = []
        for idx, lesson_data in enumerate(LESSONS_DATA):
            lesson = Lesson(
                id=uuid.uuid4(),
                course_id=course.id,
                title=lesson_data["title"],
                content_type=lesson_data["content_type"],
                duration_minutes=lesson_data["duration_minutes"],
                order_index=idx + 1,
                is_locked=idx > 0,
            )
            lessons.append(lesson)
            session.add(lesson)
        await session.flush()

        for idx, lesson in enumerate(lessons):
            test = Test(
                id=uuid.uuid4(),
                lesson_id=lesson.id,
                title=f"Тест: {lesson.title}",
                max_score=100,
                passing_score=70,
            )
            session.add(test)

            homework = Homework(
                id=uuid.uuid4(),
                lesson_id=lesson.id,
                title=f"Домашнее задание {idx + 1}",
                description=f"Выполните задания по теме '{lesson.title}'",
                due_days=7,
            )
            session.add(homework)
        await session.flush()

        tests_result = await session.execute(select(Test))
        tests = list(tests_result.scalars().all())

        hw_result = await session.execute(select(Homework))
        homeworks = list(hw_result.scalars().all())

        now = datetime.now(timezone.utc)
        students: list[Student] = []

        for student_data in STUDENTS_DATA:
            enrolled_days_ago = 30 + (hash(student_data["name"]) % 60)
            last_active_days_ago = hash(student_data["name"]) % 5 if student_data["status"] != StudentStatus.DROPPED else 15

            student = Student(
                id=uuid.uuid4(),
                name=student_data["name"],
                email=student_data["email"],
                status=student_data["status"],
                risk_score=student_data["risk_score"],
                enrolled_at=now - timedelta(days=enrolled_days_ago),
                last_active_at=now - timedelta(days=last_active_days_ago),
            )
            students.append(student)
            session.add(student)
        await session.flush()

        for student in students:
            student_data = next(s for s in STUDENTS_DATA if s["name"] == student.name)
            progress_pct = student_data["progress_pct"]
            completed_lessons = int(len(lessons) * progress_pct / 100)

            for idx, lesson in enumerate(lessons):
                if idx < completed_lessons:
                    status = ProgressStatus.COMPLETED
                    progress = 100
                elif idx == completed_lessons:
                    status = ProgressStatus.IN_PROGRESS
                    progress = 50
                else:
                    status = ProgressStatus.NOT_STARTED
                    progress = 0

                sp = StudentProgress(
                    id=uuid.uuid4(),
                    student_id=student.id,
                    course_id=course.id,
                    lesson_id=lesson.id,
                    status=status,
                    progress_percent=progress,
                    started_at=now - timedelta(days=30 - idx * 3) if status != ProgressStatus.NOT_STARTED else None,
                    completed_at=now - timedelta(days=25 - idx * 3) if status == ProgressStatus.COMPLETED else None,
                )
                session.add(sp)

            for idx, test in enumerate(tests[:completed_lessons]):
                score = 70 + (hash(f"{student.name}{idx}") % 30)
                tr = TestResult(
                    id=uuid.uuid4(),
                    student_id=student.id,
                    test_id=test.id,
                    score=score,
                    passed=score >= 70,
                    completed_at=now - timedelta(days=20 - idx * 2),
                )
                session.add(tr)

            for idx, hw in enumerate(homeworks[:completed_lessons]):
                status = SubmissionStatus.AI_CHECKED if idx < completed_lessons - 1 else SubmissionStatus.PENDING
                hs = HomeworkSubmission(
                    id=uuid.uuid4(),
                    student_id=student.id,
                    homework_id=hw.id,
                    content=f"Выполненное задание студента {student.name}",
                    status=status,
                    ai_score=75 + (hash(f"{student.name}{idx}") % 25) if status == SubmissionStatus.AI_CHECKED else None,
                    ai_feedback="Хорошая работа! Обратите внимание на использование времен." if status == SubmissionStatus.AI_CHECKED else None,
                    submitted_at=now - timedelta(days=18 - idx * 2),
                    reviewed_at=now - timedelta(days=17 - idx * 2) if status == SubmissionStatus.AI_CHECKED else None,
                )
                session.add(hs)
        await session.flush()

        demo_student = students[0]
        chat_session = ChatSession(
            id=uuid.uuid4(),
            student_id=demo_student.id,
            started_at=now - timedelta(hours=2),
        )
        session.add(chat_session)
        await session.flush()

        for idx, msg_data in enumerate(DEMO_CHAT):
            msg = ChatMessage(
                id=uuid.uuid4(),
                session_id=chat_session.id,
                role=msg_data["role"],
                content=msg_data["content"],
                response_time_ms=msg_data.get("response_time_ms"),
                resolved_by_ai=True,
                created_at=now - timedelta(hours=2) + timedelta(minutes=idx * 2),
            )
            session.add(msg)

        notifications_data = [
            {"type": NotificationType.HOMEWORK_SUBMITTED, "title": "Новое ДЗ", "message": "Иван Иванов сдал домашнее задание", "student": students[1]},
            {"type": NotificationType.STUDENT_AT_RISK, "title": "Студент в зоне риска", "message": "Мария Сидорова не активна 2 дня", "student": students[2]},
            {"type": NotificationType.LESSON_COMPLETED, "title": "Урок завершен", "message": "Александр Петров завершил урок 5", "student": students[0]},
            {"type": NotificationType.TEST_PASSED, "title": "Тест сдан", "message": "Анна Новикова сдала тест на 95 баллов", "student": students[5]},
            {"type": NotificationType.COURSE_COMPLETED, "title": "Курс завершен", "message": "Сергей Волков завершил курс!", "student": students[6]},
        ]

        for idx, notif_data in enumerate(notifications_data):
            notif = Notification(
                id=uuid.uuid4(),
                type=notif_data["type"],
                title=notif_data["title"],
                message=notif_data["message"],
                student_id=notif_data["student"].id,
                read=idx > 2,
                created_at=now - timedelta(hours=idx),
            )
            session.add(notif)

        for days_ago in range(30):
            date = (now - timedelta(days=days_ago)).date()
            base_retention = 85.0 if days_ago > 15 else 85.0 + (15 - days_ago) * 0.5
            
            metrics = DailyMetrics(
                id=uuid.uuid4(),
                date=date,
                total_students=300 + days_ago,
                active_students=int((300 + days_ago) * 0.76),
                completed_courses=280 + days_ago // 2,
                ai_questions_answered=50 + (hash(str(date)) % 30),
                ai_resolution_rate=88.0 + (hash(str(date)) % 5),
                retention_rate=base_retention,
            )
            session.add(metrics)

        await session.commit()
        print(f"Seeded: 1 course, {len(lessons)} lessons, {len(students)} students, {len(tests)} tests, {len(homeworks)} homework")


if __name__ == "__main__":
    asyncio.run(seed_database())

# E-commerce Portfolio Case

AI-автоматизация продаж для интернет-магазина на Wildberries: **+35% выручки за 21 день**.

## Demo

**Live**: [ecommerce-portfolio-case.vercel.app](https://ecommerce-portfolio-case.vercel.app)

## Результаты внедрения

| Метрика | ДО | ПОСЛЕ | Изменение |
|---------|-----|-------|-----------|
| Выручка/месяц | 2 млн ₽ | 2.7 млн ₽ | **+35%** |
| Время ответа | 15-30 мин | 30 сек | **-99.7%** |
| Потеря лидов | 40% | 5% | **-87.5%** |
| Автоматизация | 0% | 80% | **+80 п.п.** |
| Штат администраторов | 2 чел | 1 чел | **-50%** |
| ROI | — | 10 дней | — |

## Технологии

**Frontend:**
- HTML5, CSS3, JavaScript (ES6+)
- Chart.js — визуализация KPI

**Backend (AI Chat):**
- Vercel Serverless Functions
- OpenAI GPT-4o-mini

**Инфраструктура:**
- Vercel — хостинг и serverless
- GitHub — версионирование

## Структура проекта

```
case-1-ecommerce/
├── index.html          # Главная страница
├── telegram-app.html   # Демо Telegram Mini App
├── api/
│   └── chat.js         # Vercel Serverless API (OpenAI)
├── css/                # Стили и анимации
├── js/                 # Логика и графики
├── data/               # Демо-данные
├── README.md           # Документация проекта
└── PRD.md              # Product Requirements Document
```

## Запуск локально

```bash
git clone https://github.com/HiH-DimaN/ecommerce-portfolio.git
cd ecommerce-portfolio/case-1-ecommerce
npm install
npx vercel dev
```

Открыть: http://localhost:3000

> Для работы AI-чата создайте `.env.local` с `OPENAI_API_KEY=your_key`

## Документация

- [PRD.md](case-1-ecommerce/PRD.md) — полное описание продукта, требования, стек

## Контакты

**Dmitry Hihol**  
Telegram: [@dmitry_hihol](https://t.me/dmitry_hihol)

---

*Кейс демонстрирует подход к автоматизации e-commerce с измеримым ROI.*

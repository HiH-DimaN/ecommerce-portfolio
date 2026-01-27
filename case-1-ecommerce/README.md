# E-commerce Portfolio Case: AI-автоматизация продаж на Wildberries

## Демо

**Live**: [ecommerce-portfolio-case.vercel.app](https://ecommerce-portfolio-case.vercel.app/)

## О проекте

Интерактивный кейс-портфолио, демонстрирующий внедрение AI-решения для автоматизации клиентской поддержки e-commerce магазина на Wildberries.

### Бизнес-результаты (симуляция)

| Метрика | ДО | ПОСЛЕ | Изменение |
|---------|-----|-------|-----------|
| Администраторы | 2 | 1 | -50% |
| Время ответа | 30 мин | 30 сек | -99.7% |
| Потеря лидов | 40% | 5% | -87.5% |
| Автоматизация | 0% | 80% | +80 п.п. |
| Доход/месяц | 2 млн | 2.7 млн | +35% |

## Технологический стек

### Frontend (Portfolio Landing)
- **HTML5** - структура страницы
- **CSS3** - стилизация, анимации, адаптивный дизайн
- **JavaScript (ES6+)** - интерактивность, логика приложения
- **Chart.js** - визуализация графиков KPI

### Backend (AI Chat)
- **Vercel Serverless Functions** - API endpoint
- **OpenAI GPT-4o-mini** - NLP-модель для AI-ассистента

### Инфраструктура
- **Vercel** - хостинг и serverless функции
- **GitHub** - версионирование кода

## Структура проекта

```
case-1-ecommerce/
├── index.html              # Главная страница портфолио
├── telegram-app.html       # Демо Telegram Mini App
├── package.json            # Зависимости проекта
├── api/
│   └── chat.js             # Vercel Serverless API (OpenAI)
├── css/
│   ├── style.css           # Основные стили
│   ├── animations.css      # CSS-анимации
│   ├── modal.css           # Стили модальных окон
│   ├── layout-fix.css      # Фиксы layout
│   └── telegram-app.css    # Стили Telegram Mini App
├── js/
│   ├── main.js             # Основная логика приложения
│   ├── data.js             # Данные и конфигурация кейса
│   ├── charts.js           # Инициализация Chart.js графиков
│   └── telegram-app.js     # Логика Telegram Mini App демо
└── data/
    └── chat.json           # Демо-данные для fallback чата
```

## Функциональность

### 1. AI Чат-бот (Симулятор поддержки)
- Реальная интеграция с OpenAI GPT-4o-mini
- Контекстные ответы на вопросы о товарах, доставке, возврате
- Fallback на локальные ответы при недоступности API
- Отображение времени ответа

### 2. Telegram Mini App (Демо)
- Каталог товаров с фильтрацией по категориям
- Поиск товаров
- Корзина и оформление заказа
- Встроенный чат поддержки

### 3. Dashboard KPI
- Анимированные счетчики метрик
- Интерактивные графики (продажи, выручка, скорость)
- Сравнительная таблица ДО/ПОСЛЕ

### 4. Timeline внедрения
- 4 этапа: Диагностика, Разработка, Внедрение, Поддержка
- Кликабельные карточки с детализацией работ

## Локальная разработка

### Требования
- Node.js 18+
- npm или yarn

### Установка

```bash
# Клонировать репозиторий
git clone https://github.com/HiH-DimaN/ecommerce-portfolio.git
cd ecommerce-portfolio

# Установить зависимости
npm install
```

### Переменные окружения

Создайте файл `.env.local` для работы AI-чата:

```env
OPENAI_API_KEY=your_openai_api_key
```

### Запуск

```bash
# Запуск с Vercel CLI (рекомендуется для работы API)
npx vercel dev

# Или просто открыть index.html в браузере (без AI-чата)
```

## Деплой

Проект автоматически деплоится на Vercel при пуше в main ветку.

```bash
# Ручной деплой
npx vercel --prod
```

## Документация

- [PRD.md](./PRD.md) - Product Requirements Document

## Контакты

**Разработчик**: Dmitry Hihol  
**Telegram**: [@dmitry_hihol](https://t.me/dmitry_hihol)  
**GitHub**: [HiH-DimaN](https://github.com/HiH-DimaN)

---

*Версия: 1.1.0 | Январь 2026*

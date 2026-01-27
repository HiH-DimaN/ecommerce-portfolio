# WB Store Telegram Bot

AI-консультант интернет-магазина на Wildberries с интеграцией OpenAI GPT.

## Demo

**Telegram**: [@WBStoreBot_bot](https://t.me/WBStoreBot_bot)

## Возможности

- Консультация по товарам, размерам, наличию
- Информация о доставке и возврате
- Контекстный диалог (помнит историю)
- Быстрые ответы через GPT-4o-mini

## Технологии

- Python 3.11+
- aiogram 3.x — Telegram Bot API
- OpenAI GPT-4o-mini — генерация ответов
- python-dotenv — конфигурация

## Установка

```bash
cd telegram-bot
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Конфигурация

Создайте `.env` файл:

```env
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
OPENAI_API_KEY=your_openai_api_key
```

## Запуск

```bash
python bot.py
```

## Команды бота

- `/start` — начать диалог
- `/help` — справка
- `/clear` — очистить историю

## Структура

```
telegram-bot/
├── bot.py              # Основной файл бота
├── config.py           # Конфигурация и промпт
├── requirements.txt    # Зависимости
├── .env.example        # Пример переменных окружения
└── README.md
```

## Деплой

Рекомендуемые платформы:
- Railway
- Render
- VPS (systemd)

---

Связанный проект: [E-commerce Portfolio](../case-1-ecommerce/)

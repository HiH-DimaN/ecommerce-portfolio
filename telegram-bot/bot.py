import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.enums import ParseMode
from openai import AsyncOpenAI

from config import TELEGRAM_BOT_TOKEN, OPENAI_API_KEY, SYSTEM_PROMPT

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()
openai_client = AsyncOpenAI(api_key=OPENAI_API_KEY)

user_histories: dict[int, list] = {}
MAX_HISTORY = 10


async def get_ai_response(user_id: int, message: str) -> str:
    if user_id not in user_histories:
        user_histories[user_id] = []
    
    user_histories[user_id].append({"role": "user", "content": message})
    
    if len(user_histories[user_id]) > MAX_HISTORY:
        user_histories[user_id] = user_histories[user_id][-MAX_HISTORY:]
    
    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + user_histories[user_id]
    
    try:
        response = await openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            max_tokens=500,
            temperature=0.7
        )
        assistant_message = response.choices[0].message.content
        user_histories[user_id].append({"role": "assistant", "content": assistant_message})
        return assistant_message
    except Exception as e:
        logger.error(f"OpenAI error: {e}")
        return "Извините, произошла ошибка. Попробуйте позже или свяжитесь с менеджером."


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    user_histories[message.from_user.id] = []
    await message.answer(
        "👋 Привет! Я AI-консультант магазина WB Store.\n\n"
        "Помогу с выбором одежды, расскажу о наличии, размерах, доставке и возврате.\n\n"
        "Просто напишите ваш вопрос!"
    )


@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer(
        "🛍 **Чем могу помочь:**\n\n"
        "• Подобрать размер\n"
        "• Узнать о наличии товара\n"
        "• Рассказать о доставке и возврате\n"
        "• Проконсультировать по уходу за одеждой\n\n"
        "📝 Просто напишите вопрос!",
        parse_mode=ParseMode.MARKDOWN
    )


@dp.message(Command("clear"))
async def cmd_clear(message: types.Message):
    user_histories[message.from_user.id] = []
    await message.answer("🔄 История диалога очищена. Начнём сначала!")


@dp.message()
async def handle_message(message: types.Message):
    if not message.text:
        return
    
    await bot.send_chat_action(message.chat.id, "typing")
    response = await get_ai_response(message.from_user.id, message.text)
    await message.answer(response)


async def main():
    logger.info("Bot starting...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

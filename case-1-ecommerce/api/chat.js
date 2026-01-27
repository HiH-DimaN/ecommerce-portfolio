import OpenAI from 'openai';

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

const SYSTEM_PROMPT = `Ты — AI-консультант интернет-магазина одежды на Wildberries.

Твои задачи:
- Отвечать на вопросы о товарах, наличии, размерах
- Помогать с выбором товара
- Информировать о доставке и возврате
- Консультировать по уходу за одеждой

Информация о магазине:
- Магазин: WB Store — женская и мужская одежда
- Доставка: бесплатно от 500 ₽, пункты Wildberries 2-3 дня
- Возврат: 14 дней, бесплатно через пункты WB
- Размеры: XS-XXL, есть размерная сетка
- Средний чек: 3000 ₽

Стиль общения:
- Дружелюбный, но профессиональный
- Краткие и чёткие ответы (2-3 предложения максимум)
- Если не знаешь точного ответа — предложи связаться с менеджером
- Используй эмодзи умеренно

Отвечай на русском языке.`;

export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const { message, history = [] } = req.body;

    if (!message) {
      return res.status(400).json({ error: 'Message is required' });
    }

    const messages = [
      { role: 'system', content: SYSTEM_PROMPT },
      ...history.slice(-10),
      { role: 'user', content: message }
    ];

    const completion = await openai.chat.completions.create({
      model: 'gpt-4o-mini',
      messages,
      max_tokens: 300,
      temperature: 0.7,
    });

    const reply = completion.choices[0].message.content;

    return res.status(200).json({ reply });
  } catch (error) {
    console.error('OpenAI error:', error);
    return res.status(500).json({ 
      error: 'Извините, произошла ошибка. Попробуйте позже.' 
    });
  }
}

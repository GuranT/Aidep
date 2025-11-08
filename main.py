import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import aiohttp

# Настройки
BOT_TOKEN = os.environ['BOT_TOKEN']
DEEPSEEK_KEY = os.environ['DEEPSEEK_API_KEY']

# Команда /start
async def start(update, context):
    await update.message.reply_text(
        "🤖 Привет! Я AI-помощник DeepSeek.\n"
        "Просто напиши вопрос - и я отвечу!"
    )

# Обработка сообщений
async def handle_message(update, context):
    user_text = update.message.text
    
    # Показываем "печатает..."
    await update.message.chat.send_action(action="typing")
    
    try:
        # Запрос к DeepSeek
        headers = {
            "Authorization": f"Bearer {DEEPSEEK_KEY}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "deepseek-chat",
            "messages": [{"role": "user", "content": user_text}],
            "max_tokens": 2000
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://api.deepseek.com/v1/chat/completions",
                json=data,
                headers=headers
            ) as response:
                result = await response.json()
                answer = result["choices"][0]["message"]["content"]
                await update.message.reply_text(answer)
                
    except Exception as e:
        await update.message.reply_text("❌ Ошибка, попробуй еще раз")

# Запуск бота
app = Application.builder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT, handle_message))

print("🤖 Бот запущен!")
app.run_polling()

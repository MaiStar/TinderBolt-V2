from telegram.ext import ApplicationBuilder, MessageHandler, filters, CallbackQueryHandler, CommandHandler

from gpt import *
from util import *

# тут будем писать наш код :)


async def hello(update, context):
    await send_text(update, context, "Привет!")
    await send_text_buttons(update, context, "Выберите режим работы", {  # Текст перед кнопкой
        "btn_start": " Старт ",  # Текст и команда кнопки "Старт"
        "btn_stop": " Стоп "  # Текст и команда кнопки "Стоп"
    })

# Добавляем хендлер для команды /start


async def start(update, context):
    await hello(update, context)

if __name__ == "__main__":
    print("🚀 Бот запускается...")  # Статус запуска

    app = ApplicationBuilder().token(
        "6464706338:AAHlWtteKxxy9wDHKVjwygoj4hycZ3CU8FY").build()

    # Добавляем хендлеры
    app.add_handler(CommandHandler("start", start))
    # Можно добавить обработчик для всех текстовых сообщений, если нужно
    # app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, some_handler))

    print("✅ Бот запущен! Отправьте /start в чат с ботом для теста.")
    print("Для остановки: Ctrl+C")

    # drop_pending_updates=True — игнорирует старые сообщения при рестарте
    app.run_polling(drop_pending_updates=True)

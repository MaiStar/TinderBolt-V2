from telegram.ext import ApplicationBuilder, MessageHandler, filters, CallbackQueryHandler, CommandHandler

from gpt import *
from util import *

# тут будем писать наш код :)


async def hello(update, context):
    # Отправляем приветствие с кнопками (как раньше)
    await send_text(update, context, "Привет!")
    await send_text_buttons(update, context, "Выберите режим работы", {  # Текст перед кнопкой
        "btn_start": " Старт ",  # Текст и команда кнопки "Старт"
        "btn_stop": " Стоп "  # Текст и команда кнопки "Стоп"
    })


async def start(update, context):
    # Отправляем картинку по команде /start
    await send_photo(update, context, "main")

# Обработка кнопок (для всех callback-запросов)


async def hello_button(update, context):
    query = update.callback_query
    await query.answer()  # Подтверждаем нажатие (чтобы убрать "часики")

    if query.data == "btn_start":
        await send_text(update, context, "Режим 'Старт' активирован!")
    elif query.data == "btn_stop":
        await send_text(update, context, "Режим 'Стоп' активирован!")
    # Можно добавить больше логики (например, отправку фото или вызов GPT)

if __name__ == "__main__":
    print("🚀 Бот запускается...")

    app = ApplicationBuilder().token(
        "6464706338:AAHlWtteKxxy9wDHKVjwygoj4hycZ3CU8FY").build()

    # Хендлер для команды /start — отправляет фото
    app.add_handler(CommandHandler("start", start))

    # Хендлер для обычных текстовых сообщений (исключая команды) — вызывает hello
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, hello))

    # Хендлер для нажатий на кнопки (без pattern — для всех)
    app.add_handler(CallbackQueryHandler(hello_button))

    print("✅ Бот запущен! Отправьте /start в чат для теста (получите картинку).")
    print("Для остановки: Ctrl+C")

    app.run_polling(drop_pending_updates=True)

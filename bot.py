from telegram.ext import ApplicationBuilder, MessageHandler, filters, CallbackQueryHandler, CommandHandler

from gpt import *
from util import *

# Глобальная переменная для режима диалога


class Dialog:
    def __init__(self):
        self.mode = "main"


dialog = Dialog()

# Инициализация ChatGPT
chatgpt = ChatGptService(token="javcgk8pFZZssAv/GAaLFtpU2XRxcYwvevXZIyGFAmFZI3L06qepS/RV1vwI5WWJCzXUXxhEgBL78gsqw097AFLgJhfSJIYTGLJXuNmmC1WHnD5rLqK5bovPAMquTedVct0tMO3YKL7WnwWVBYot49YP/DsQPPKt8po+UHHV7OmqYXjjYWW2CcTundXGhGuyvJm5sNKlWWp5DZqBhLIWahLjBMGuOH0m3XMutHaIG8dtbZZqI=")


async def hello(update, context):
    if dialog.mode == "gpt":
        await gpt_dialog(update, context)
    else:
        # Отправляем приветствие с кнопками (как раньше)
        await send_text(update, context, "Привет!")
        await send_text_buttons(update, context, "Выберите режим работы", {  # Текст перед кнопкой
            "btn_start": " Старт ",  # Текст и команда кнопки "Старт"
            "btn_stop": " Стоп "  # Текст и команда кнопки "Стоп"
        })
        await show_main_menu(update, context, {
            "start": "главное меню бота",
            "profile": "генерация Tinder-профиля 😎",
            "opener": "сообщение для знакомства 🥰",
            "message": "переписка от вашего имени 😈",
            "date": "переписка со звездами 🔥",
            "gpt": "задать вопрос ChatGPT 🧠"
        })


async def start(update, context):
    dialog.mode = "main"
    text = load_message("main")
    await send_photo(update, context, "main")
    await send_text(update, context, text)
    await show_main_menu(update, context, {
        "start": "главное меню бота",
        "profile": "генерация Tinder-профиля 😎",
        "opener": "сообщение для знакомства 🥰",
        "message": "переписка от вашего имени 😈",
        "date": "переписка со звездами 🔥",
        "gpt": "задать вопрос ChatGPT 🧠"
    })


async def gpt(update, context):
    dialog.mode = "gpt"
    await send_photo(update, context, "gpt")
    await send_text(update, context, "Напишите сообщение *ChatGPT*:")
    await show_main_menu(update, context, {
        "start": "главное меню бота",
        "profile": "генерация Tinder-профиля 😎",
        "opener": "сообщение для знакомства 🥰",
        "message": "переписка от вашего имени 😈",
        "date": "переписка со звездами 🔥",
        "gpt": "задать вопрос ChatGPT 🧠"
    })


async def gpt_dialog(update, context):
    prompt = load_prompt("gpt")
    text = update.message.text
    answer = await chatgpt.send_question(prompt, text)
    await send_text(update, context, answer)


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
        "6597079317:AAFMCwtle2wRhd4BF4GugepZj01VyF8asNA").build()

    # Хендлер для команды /start — отправляет фото
    app.add_handler(CommandHandler("start", start))

    # Хендлер для команды /gpt
    app.add_handler(CommandHandler("gpt", gpt))

    # Хендлер для обычных текстовых сообщений (исключая команды) — вызывает hello
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, hello))

    # Хендлер для нажатий на кнопки (без pattern — для всех)
    app.add_handler(CallbackQueryHandler(hello_button))

    print("✅ Бот запущен! Отправьте /start в чат для теста (получите картинку).")
    print("Для остановки: Ctrl+C")

    app.run_polling(drop_pending_updates=True)

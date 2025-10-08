from telegram.ext import ApplicationBuilder, MessageHandler, filters, CallbackQueryHandler, CommandHandler

from gpt import *
from util import *

# Глобальная переменная для режима диалога


class Dialog:
    def __init__(self):
        self.mode = "main"
        self.list = []


dialog = Dialog()

# Инициализация ChatGPT
chatgpt = ChatGptService(token="javcgk8pFZZssAv/GAaLFtpU2XRxcYwvevXZIyGFAmFZI3L06qepS/RV1vwI5WWJCzXUXxhEgBL78gsqw097AFLgJhfSJIYTGLJXuNmmC1WHnD5rLqK5bovPAMquTedVct0tMO3YKL7WnwWVBYot49YP/DsQPPKt8po+UHHV7OmqYXjjYWW2CcTundXGhGuyvJm5sNKlWWp5DZqBhLIWahLjBMGuOH0m3XMutHaIG8dtbZZqI=")


async def hello(update, context):
    if dialog.mode == "gpt":
        await gpt_dialog(update, context)
    elif dialog.mode == "date":
        await date_dialog(update, context)
    elif dialog.mode == "message":
        await message_dialog(update, context)
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
    my_message = await send_text(update, context, "ChatGPT думает. Ожидайте...")
    prompt = load_prompt("gpt")
    text = update.message.text
    answer = await chatgpt.send_question(prompt, text)
    await my_message.edit_text(answer)


async def date(update, context):
    dialog.mode = "date"
    await send_photo(update, context, "date")
    text = load_message("date")
    await send_text_buttons(update, context, text, {
        "date_monro": " Мерилин Монро",
        "date_obama": "Мишель Обама",
        "date_kennedy": "Жаклин Кеннеди"
    })
    await show_main_menu(update, context, {
        "start": "главное меню бота",
        "profile": "генерация Tinder-профиля 😎",
        "opener": "сообщение для знакомства 🥰",
        "message": "переписка от вашего имени 😈",
        "date": "переписка со звездами 🔥",
        "gpt": "задать вопрос ChatGPT 🧠"
    })


async def date_dialog(update, context):
    text = update.message.text
    my_message = await send_text(update, context, "Девушка набирает текст...")
    answer = await chatgpt.add_message(text)
    await my_message.edit_text(answer)


async def date_button(update, context):
    query = update.callback_query
    data = query.data
    await query.answer()
    await send_photo(update, context, data)
    await send_text(update, context, " Отличный выбор! ")
    prompt = load_prompt(data)
    chatgpt.set_prompt(prompt)


async def message(update, context):
    dialog.mode = "message"
    await send_photo(update, context, "message")
    text = load_message("message")
    await send_text_buttons(update, context, text, {
        "message_next": "Написать сообщение",
        "message_date": "Пригласить на свидание",
    })
    dialog.list.clear()
    await show_main_menu(update, context, {
        "start": "главное меню бота",
        "profile": "генерация Tinder-профиля 😎",
        "opener": "сообщение для знакомства 🥰",
        "message": "переписка от вашего имени 😈",
        "date": "переписка со звездами 🔥",
        "gpt": "задать вопрос ChatGPT 🧠"
    })


async def message_dialog(update, context):
    text = update.message.text
    dialog.list.append(text)


async def message_button(update, context):
    query = update.callback_query
    data = query.data
    await query.answer()
    prompt = load_prompt(data)
    user_chat_history = "\n\n".join(dialog.list)
    my_message = await send_text(update, context, "ChatGPT думает над вариантами ответа...")
    answer = await chatgpt.send_question(prompt, user_chat_history)
    await my_message.edit_text(answer)


# Обработка кнопок (для всех callback-запросов, кроме date_ и message_)
async def hello_button(update, context):
    query = update.callback_query
    await query.answer()  # Подтверждаем нажатие (чтобы убрать "часики")

    data = query.data

    if data == "btn_start":
        await send_text(update, context, "Режим 'Старт' активирован!")
    elif data == "btn_stop":
        await send_text(update, context, "Режим 'Стоп' активирован!")
    elif data == "start":
        await start(update, context)
    elif data == "gpt":
        await gpt(update, context)
    elif data == "date":
        await date(update, context)
    elif data == "message":
        await message(update, context)
    elif data == "profile":
        await send_text(update, context, "Функция в разработке!")
    elif data == "opener":
        await send_text(update, context, "Функция в разработке!")

if __name__ == "__main__":
    print("🚀 Бот запускается...")

    app = ApplicationBuilder().token(
        "6597079317:AAFMCwtle2wRhd4BF4GugepZj01VyF8asNA").build()

    # Хендлер для команды /start — отправляет фото
    app.add_handler(CommandHandler("start", start))

    # Хендлер для команды /gpt
    app.add_handler(CommandHandler("gpt", gpt))

    # Хендлер для команды /date
    app.add_handler(CommandHandler("date", date))

    # Хендлер для команды /message
    app.add_handler(CommandHandler("message", message))

    # Хендлер для обычных текстовых сообщений (исключая команды) — вызывает hello
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, hello))

    # Хендлер для нажатий на кнопки (основные)
    app.add_handler(CallbackQueryHandler(hello_button))

    # Хендлер для кнопок date
    app.add_handler(CallbackQueryHandler(date_button, pattern="^date_.*"))

    # Хендлер для кнопок message
    app.add_handler(CallbackQueryHandler(
        message_button, pattern="^message_.*"))

    print("✅ Бот запущен! Отправьте /start в чат для теста (получите картинку).")
    print("Для остановки: Ctrl+C")

    app.run_polling(drop_pending_updates=True)

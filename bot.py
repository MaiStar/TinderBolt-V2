from telegram.ext import ApplicationBuilder, MessageHandler, filters, CallbackQueryHandler, CommandHandler

from gpt import *
from util import *

# тут будем писать наш код :)


app = ApplicationBuilder().token(
    "6464706338:AAHlWtteKxxy9wDHKVjwygoj4hycZ3CU8FY").build()
app.run_polling()

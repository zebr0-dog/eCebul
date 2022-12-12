from aiogram.types import Update

from main import bot, dp

async def error_notify(update: Update, exception):
    tag = ""
    id = 0
    chat = 0
    if "callback_query" in update:
        tag = update.callback_query.from_user.username
        id = update.callback_query.from_user.id
        chat = update.callback_query.message.chat.id
        await update.callback_query.message.reply("Нахуй йди, оке?")
    elif "message" in update:
        tag = update.message.from_user.username
        id = update.message.from_user.id
        chat = update.message.chat.id
        await update.message.reply("Нахуй йди, оке?")
    else:
        tag = "error"
        id=1
        chat = 1
    #await bot.send_message(652289955, "Йди нахуй")
    state = dp.current_state(chat=chat, user=id)
    await state.finish()
    

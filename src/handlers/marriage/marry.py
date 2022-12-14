from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup

import texts
import buttons

from main import DB

async def marriage_proposal(msg: Message):
    username = msg.from_user.id
    await msg.reply_to_message.reply(
        texts.PROPOSAL_TEXT.format(
            username,
        ),
        reply_markup=buttons.marriage_buttons(msg.from_user.id, msg.reply_to_message.from_user.id)
    )

async def marriage_declined(query: CallbackQuery):
    await query.answer()
    data = query.data.split(":")
    if int(data[-1]) == query.from_user.id:
        await query.message.reply("Пропозицію шлюбу відхилено")
        await query.message.edit_reply_markup(InlineKeyboardMarkup())

async def marriage_accepted(query: CallbackQuery):
    await query.answer()
    data = query.data.split(":")
    id1, id2 = int(data[1]), int(data[2])
    if query.from_user.id == id2:
        res = await DB.marry(id1=id1, id2=id2)  # type: ignore
        await query.message.reply_to_message.reply(texts.MARRIAGE_RESULTS[res])
        await query.message.edit_reply_markup(InlineKeyboardMarkup())
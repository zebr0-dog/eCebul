from aiogram.types import Message

import texts

from main import DB

async def divorce_process(msg: Message):
    divorce_res = await DB.divorce(msg.from_user.id, msg.reply_to_message.from_user.id)
    await msg.reply(texts.DIVORCE_RESULTS[divorce_res])
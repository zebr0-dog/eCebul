from aiogram.types import Message

import db
import texts

async def divorce_process(msg: Message):
    divorce_res = await db.divorce(msg.from_user.id, msg.reply_to_message.from_user.id)
    await msg.reply(texts.DIVORCE_RESULTS[divorce_res])
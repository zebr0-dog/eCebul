from aiogram.types import Message

import db

async def show_partyies(msg: Message):
    list_of_partyies = await db.get_all_partyies()
    if list_of_partyies:
        text = ""
        for name, owner in list_of_partyies:
            owner_pass = await db.get_passport(owner)
            owner_name = owner_pass[0]
            text = "\n".join([text, name, "(", owner_name, ")"])
        await msg.reply(text)
    else:
        await msg.reply("Поки партій нема. Створіть першу!")
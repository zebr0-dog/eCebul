from aiogram.types import Message

import db

async def show_partyies(msg: Message):
    list_of_partyies = await db.get_all_partyies()
    if list_of_partyies:
        text = ""
        for name in list_of_partyies:
            owner = list_of_partyies[name]
            owner_pass = await db.get_passport(owner)
            owner_name = owner_pass[0]
            text = "".join([text, "\n", name, "(", owner_name, ")"])
        await msg.reply(text)
    else:
        await msg.reply("Поки партій нема. Створіть першу!")
from aiogram.types import Message

import db
import texts

async def show_partyies(msg: Message):
    list_of_partyies = await db.get_all_partyies()
    if list_of_partyies:
        text = "<b>Політичні партії\nКавуневої Республіки\n</b>"
        for party in list_of_partyies:
            party_text = texts.PARTYIES[1].format(
                name=party,
                username=list_of_partyies[party]["owner"]["username"][1::],
                owner=list_of_partyies[party]["owner"]["name"],
                members_count=list_of_partyies[party]["members_count"]
            )
            text = "".join([text, party_text])
        await msg.reply(text)
    else:
        await msg.reply("Поки партій нема. Створіть першу!")
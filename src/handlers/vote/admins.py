import imp
from aiogram.types import Message

import db

from main import bot

async def start_reg_candidats(msg: Message):
    await db.change_status_of_vote(2)
    await msg.answer("Розпочалась реєстрація кандидатів на голосування")
    message = await bot.send_message(-1001204415902, "Розпочалась реєстрація кандидатів в сейм. !балатуватись в ПП бота")
    await message.pin(disable_notification=False)

async def start_voting(msg: Message):
    await db.change_status_of_vote(3)
    await msg.answer("Розпочались вибори в сейм")
    message = await bot.send_message(-1001204415902, "Розпочались вибори в сейм. !голосувати в ПП бота")
    await message.pin(disable_notification=False)

async def final_voting(msg: Message):
    res = await db.change_status_of_vote(1)
    await msg.answer("Голосування завершено, я вишлю результати в головний чат")
    text = ""
    for candidat in res:
        text = "".join([
            text,
            res[candidat]["name"],
            " ",
            res[candidat]["surname"],
            " - ",
            str(res[candidat]["votes"]),
            "\n"
        ])
    message = await bot.send_message(-1001204415902, text)
    await message.pin(disable_notification=False)
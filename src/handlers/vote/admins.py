import imp
from aiogram.types import Message

import db
import texts

from main import bot, MAIN_CHAT

async def start_reg_candidats(msg: Message):
    await db.change_status_of_vote(2)
    await msg.answer("Розпочалась реєстрація кандидатів на голосування")
    message = await bot.send_message(
        MAIN_CHAT,
        texts.REGISTRATION_WAS_STARTED
    )
    await message.pin(disable_notification=False)

async def start_voting(msg: Message):
    await db.change_status_of_vote(3)
    await msg.answer("Розпочались вибори в сейм")
    message = await bot.send_message(
        MAIN_CHAT,
        texts.VOTING_WAS_STARTED
    )
    await message.pin(disable_notification=False)

async def final_voting(msg: Message):
    res = await db.change_status_of_vote(1)
    await msg.answer("Голосування завершено, я вишлю результати в головний чат")
    text = ""
    for id in res:
        text = "\n\n".join([
            text,
            texts.FINAL_RES.format(
                username=res[id]["username"],
                name=res[id]["name"],
                surname=res[id]["surname"],
                votes=res[id]["votes"]
            ),
        ])
    message = await bot.send_message(MAIN_CHAT, text)
    await message.pin(disable_notification=False)
from aiogram.types import Message

import texts

from main import bot, MAIN_CHAT, DB

async def start_reg_candidats(msg: Message):
    await DB.change_status_of_vote(2)
    await msg.answer("Розпочалась реєстрація кандидатів на голосування")
    message = await bot.send_message(
        MAIN_CHAT,
        texts.REGISTRATION_WAS_STARTED
    )
    await message.pin(disable_notification=False)

async def start_voting(msg: Message):
    await DB.change_status_of_vote(3)
    await msg.answer("Розпочались вибори")
    message = await bot.send_message(
        MAIN_CHAT,
        texts.VOTING_WAS_STARTED
    )
    await message.pin(disable_notification=False)

async def final_voting(msg: Message):
    res = await DB.change_status_of_vote(1)
    await msg.answer("Голосування завершено, я вишлю результати в головний чат")
    text = ""
    if res:
        for id, candidate in res.items():
            text = "\n\n".join([
                text,
                texts.FINAL_RES.format(
                    username=candidate.username,
                    name=candidate.name,
                    surname=candidate.surname,
                    votes=candidate.votes
                ),
            ])
        message = await bot.send_message(MAIN_CHAT, text)
        await message.pin(disable_notification=False)
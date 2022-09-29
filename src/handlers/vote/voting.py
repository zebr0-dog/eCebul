from aiogram.types import Message, CallbackQuery

import db
import texts
import buttons

async def list_of_candidats(msg: Message):
    candidates = await db.get_all_candidats()
    if type(candidates) == dict:
        await msg.answer(
            "Список кандидатів. Натисніть кнопку, щоб побачити більше подробиць про кандидата",
            reply_markup=buttons.candidates_keyboard(candidates)
        )
    else:
        await msg.answer("Наразі голосування неможливе")

async def get_candidat_info(cb: CallbackQuery):
    await cb.answer()
    id = int(cb.data.removeprefix("can:"))
    candidat = await db.get_candidate(id)
    if type(candidat) == dict:
        await cb.message.delete()
        if candidat["party"] == None:
            candidat["party"] = "Позапартійний"
        await cb.message.answer(
            texts.CANDIDAT_PROFILE.format(
                name=candidat["name"],
                surname=candidat["surname"],
                program=candidat["program"],
                party=candidat["party"],
                username=candidat["username"]
            ),
            reply_markup=buttons.vote(id)
        )

async def vote(cb: CallbackQuery):
    await cb.answer()
    id = int(cb.data.removeprefix("vote:"))
    res = await db.vote(id, cb.from_user.id)
    if res == 0:
        await cb.message.delete()
        await cb.message.answer("Ви успішно проголосували")
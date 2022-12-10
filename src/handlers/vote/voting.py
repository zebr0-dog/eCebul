from aiogram.types import Message, CallbackQuery

import texts
import buttons

from main import DB

async def list_of_candidates(msg: Message):
    candidates = await DB.get_all_candidats()
    if type(candidates) == dict:
        await msg.answer(
            "Список кандидатів. Натисніть кнопку, щоб побачити більше подробиць про кандидата",
            reply_markup=buttons.candidates_keyboard(candidates)  # type: ignore
        )
    else:
        await msg.answer("Наразі голосування неможливе")

async def get_candidate_info(cb: CallbackQuery):
    await cb.answer()
    id = int(cb.data.removeprefix("can:"))
    candidate = await DB.get_candidate(id)
    if type(candidate) == dict:
        await cb.message.delete()
        if candidate.party == None:  # type: ignore
            candidate.party = "Позапартійний"  # type: ignore
        await cb.message.answer(
            texts.CANDIDAT_PROFILE.format(
                name=candidate.name,  # type: ignore
                surname=candidate.surname, # type: ignore
                program=candidate.program, # type: ignore
                party=candidate.party, # type: ignore
                username=candidate.username # type: ignore
            ),
            reply_markup=buttons.vote(id)
        )

async def vote(cb: CallbackQuery):
    await cb.answer()
    id = int(cb.data.removeprefix("vote:"))
    res = await DB.vote(id, cb.from_user.id)
    if res == 0:
        await cb.message.delete()
        await cb.message.answer("Ви успішно проголосували")
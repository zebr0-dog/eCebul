from aiogram.types import Message
from aiogram.dispatcher import FSMContext

import states

from main import DB

async def start_reg(msg: Message):
    await msg.answer("Будь-ласка, надішліть свою передвиборчу програму. Не більше 250 символів")
    await states.RegCandidate.program.set()

async def get_program(msg: Message, state: FSMContext):
    if len(msg.text.strip(".,!?\n ")) <= 250:
        save = await DB.save_candidate(msg.from_user.id, msg.text)
        if not save:
            await msg.answer("Ви зареєструвались на участь в виборах")
        else:
            await msg.answer("Наразі реєстрація неможлива")
    else:
        await msg.answer("Ваша програма задовга. Зареєструйтесь спочатку")
    await state.finish()
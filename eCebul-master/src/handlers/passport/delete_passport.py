from aiogram.types import Message
from aiogram.dispatcher import FSMContext

import states
import db

async def delete_passport_start(message: Message):
        await message.answer("<b>Надішліть ID користувача для позбавлення громадянства.</b>")
        await states.DeletePassport.delete_pass.set()

async def delete_passport(message: Message, state: FSMContext):
    await db.delete_passport(int(message.text))
    await message.answer("<b>Користувача видалено!</b>")
    await state.finish()
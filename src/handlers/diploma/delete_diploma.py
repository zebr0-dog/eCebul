from aiogram.types import Message
from aiogram.dispatcher import FSMContext

import states

from main import DB

async def delete_diploma_start(message: Message):
        await message.answer("<b>Надішліть ID користувача для видалення диплома.</b>")
        await states.DeleteDiploma.delete_diploma.set()

async def delete_diploma(message: Message, state: FSMContext):
    await DB.delete_diploma(int(message.text))
    await message.answer("<b>Диплом видален!</b>")
    await state.finish()

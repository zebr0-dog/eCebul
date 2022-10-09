from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext

import texts
import states
import db
import buttons

async def change_help(message: Message, lor: int):
    await states.ChangePasspost.column_pass.set()
    await message.answer(texts.CHANGE_PASSPORT, reply_markup=buttons.change_kb_gen(lor))

async def change_start(message: Message, state: FSMContext):
    await state.update_data(column=message.text)
    await message.answer(
        texts.REQUEST_ID.format(
            column=message.text
        ),
        reply_markup=ReplyKeyboardRemove()
    )
    await states.ChangePasspost.id_pass.set()

async def get_id(message: Message, state: FSMContext):
        target_id = message.text
        exist_user = await db.check_is_user_exist(target_id)
        if not exist_user:
            await message.answer(texts.PASSPORT_DO_NOT_EXIST)
        else:
            allowed_changing = (
                "ім'я",
                "прізвище",
                "стать",
                "тег",
                "баланс",
                "інфо",
                "робота"
            )
            data = await state.get_data()
            changing_column = data.get("column", "")
            if changing_column in allowed_changing:
                await state.update_data(target=target_id)
                keyboards = {
                    "інфо": buttons.change_info,
                    "робота": buttons.job_reg
                }
                keyboard = keyboards.get(changing_column, ReplyKeyboardRemove())
                await message.answer(
                    "Введіть нові дані або оберіть з клавіатури:",
                    reply_markup=keyboard
                )
                await states.ChangePasspost.change_data_pass.set()
            else:
                await state.finish()
                await message.answer("Помилка. Почніть спочатку.", reply_markup=ReplyKeyboardRemove())

async def get_new_data(message: Message, state: FSMContext):
        new_data = message.text
        data = await state.get_data()
        target = data.get('target')
        column = data.get("column")
        columns = {
            "ім'я": "name",
            "прізвище": "surname",
            "стать": "sex",
            "тег": "username",
            "баланс": "balance",
            "інфо": "info",
            "робота": "job",
            "емодзі": "emoji"
        }
        await state.finish()
        if (await db.update_data(columns[column], target, new_data)) == 0:
            await message.answer("<b>OK</b>", reply_markup=ReplyKeyboardRemove())
        else:
            await message.answer("Помилка. Почніть спочатку.", reply_markup=ReplyKeyboardRemove())
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext

import texts
import states
import buttons
import variables

from main import DB

async def change_help(message: Message):
    await states.ChangePasspost.column_pass.set()
    await message.answer(texts.CHANGE_PASSPORT, reply_markup=buttons.change_kb_gen())

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
        exist_user = await DB.get_passport(id=int(target_id))
        if not exist_user:
            await message.answer(texts.PASSPORT_DO_NOT_EXIST)
            return
        else:
            allowed_changing = (
                "ім'я",
                "прізвище",
                "стать",
                "тег",
                "баланс",
                "статус",
                "громадянство",
                "робота",
                "емодзі",
                "дата_народження"
            )
            data = await state.get_data()
            changing_column = data.get("column", "")
            if changing_column in allowed_changing:
                await state.update_data(target=target_id)
                keyboards = {
                    "стать": buttons.sex_keyboard,
                    "статус": buttons.status_keyboard,
                    "громадянство": buttons.citizenship_keyboard,
                    "робота": buttons.job_keyboard
                }
                keyboard = keyboards.get(changing_column, ReplyKeyboardRemove)
                await message.answer(
                    "Введіть нові дані або оберіть з клавіатури:",
                    reply_markup=keyboard()  # type: ignore
                )
                await states.ChangePasspost.change_data_pass.set()
            else:
                await state.finish()
                await message.answer("Помилка. Почніть спочатку.", reply_markup=ReplyKeyboardRemove())

async def get_new_data(message: Message, state: FSMContext):
        new_data = message.text
        data = await state.get_data()
        target = int(data.get('target'))  # type: ignore
        column = data.get("column")
        columns = {
            "ім'я": {"column": "name", "value": None},
            "прізвище": {"column": "surname", "value": None},
            "стать": {"column": "sex", "value": {"Чоловік": 1, "Жінка": 2}},
            "громадянство": {"column": "citizenship", "value": {"Громадянин": True, "Негромадянин": False}},
            "тег": {"column": "username", "value": None},
            "баланс": {"column": "balance", "value": None},
            "статус": {"column": "status", "value": variables.STATUSES},
            "робота": {"column": "job", "value": variables.JOBS},
            "емодзі": {"column": "emoji", "value": None},
            "дата_народження": {"column": "birthdate", "value": None}
        }
        await state.finish()
        current_data = columns.get(column)  # type: ignore
        
        if current_data:
            if current_data["value"]:
                data = current_data["value"][new_data]
            else:
                data = new_data
            result = await DB.update_passport(column=current_data["column"], id=target, data=data)
            if not result:
                await message.answer(f"Дані оновлено", reply_markup=ReplyKeyboardRemove())
                return
        await message.answer(f"Помилка. Почніть спочатку", reply_markup=ReplyKeyboardRemove())

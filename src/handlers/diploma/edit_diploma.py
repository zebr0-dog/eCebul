from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext

import texts
import states
import buttons
import variables

from main import DB

async def change_help(message: Message):
    await states.ChangeDiploma.column_pass.set()
    await message.answer(texts.CHANGE_PASSPORT, reply_markup=buttons.change_kb_gen(variables.ALLOWED_DIPLOMA_CHANGES))

async def change_start(message: Message, state: FSMContext):
    await state.update_data(column=message.text)
    await message.answer(
        texts.REQUEST_ID.format(
            column=message.text
        ),
        reply_markup=ReplyKeyboardRemove()
    )
    await states.ChangeDiploma.id_pass.set()

async def get_id(message: Message, state: FSMContext):
        target_id = message.text
        exist_user = await DB.get_diploma(user_id=int(target_id))
        if not exist_user:
            await message.answer(texts.DIPLOMA_DO_NOT_EXIST)
            return
        else:
            allowed_changing = (
                "ім'я",
                "прізвище",
                "назва_академії",
                "дата_початку_навчання",
                "дата_закінчення_навчання",
                "середня_оцінка"
            )
            data = await state.get_data()
            changing_column = data.get("column", "")
            if changing_column in allowed_changing:
                await state.update_data(target=target_id)
                await message.answer("Введіть нові дані:") #type: ignor
                await states.ChangeDiploma.change_data_diploma.set()
            else:
                await state.finish()
                await message.answer("Помилка. Почніть спочатку.", reply_markup=ReplyKeyboardRemove())

async def get_new_data(message: Message, state: FSMContext):
        new_data = message.text
        data = await state.get_data()
        target = int(data.get('target'))  # type: ignore
        column = data.get("column")
        columns = {
            "ім'я": {"column": "student_name", "value": None},
            "прізвище": {"column": "student_surname", "value": None},
            "назва_академії": {"column": "academy_name", "value": None},
            "дата_початку_навчання": {"column": "date_course_start", "value": None},
            "дата_закінчення_навчання": {"column": "date_course_end", "value": None},
            "середня_оцінка": {"column": "average_grade", "value": None},
        }
        await state.finish()
        current_data = columns.get(column)  # type: ignore
        if current_data:
            if current_data["value"]: data = current_data["value"][new_data]
            else: data = new_data
            result = await DB.update_diploma(column=current_data["column"], id=target, data=data)
            if not result:
                await message.answer(f"Дані оновлено", reply_markup=ReplyKeyboardRemove())
                return
        await message.answer(f"Помилка. Почніть спочатку", reply_markup=ReplyKeyboardRemove())

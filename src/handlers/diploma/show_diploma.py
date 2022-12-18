from pyexpat.errors import messages
from aiogram.types import Message
from datetime import date

import texts
import variables

from main import DB

async def show_diploma(message: Message):
    diploma = await DB.get_diploma(user_id=message.from_user.id)
    if diploma:
        text = texts.DIPLOMA.format(
            user_id = diploma.user_id,
            student_name = diploma.student_name,
            student_surname = diploma.student_surname,
            academy_name = diploma.academy_name,
            date_course_start = date.fromisoformat(diploma.date_course_start).strftime("%d.%m.%Y"),
            date_course_end = date.fromisoformat(diploma.date_course_end).strftime("%d.%m.%Y"),
            average_grade = diploma.average_grade
        )
        await message.answer(text)
    else:
        await message.answer(texts.DIPLOMA_DO_NOT_EXIST)

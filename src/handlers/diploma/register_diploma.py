from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.utils.exceptions import CantInitiateConversation, CantTalkWithBots
from aiogram.dispatcher import FSMContext

import texts
import buttons
import states
import variables
from main import bot, LOG_CHANNEL, DB

async def give(message: Message):
    await states.GiveDiploma.user_id_pass.set()
    await message.answer(text=texts.DIPLOMA_REGISTRATION_STEPS[0])

async def giving_user_id(message: Message, state: FSMContext):
    await state.update_data(user_id=message.text)
    await states.GiveDiploma.next()
    await message.answer(text=texts.DIPLOMA_REGISTRATION_STEPS[1])

async def giving_student_name(message: Message, state: FSMContext):
    async with state.proxy() as data: data['student_name'] = message.text
    await states.GiveDiploma.next()
    await message.answer(text=texts.DIPLOMA_REGISTRATION_STEPS[2])

async def giving_student_surname(message: Message, state: FSMContext):
    async with state.proxy() as data: data['student_surname'] = message.text
    await states.GiveDiploma.next()
    await message.answer(text=texts.DIPLOMA_REGISTRATION_STEPS[3])

async def giving_academy_name(message: Message, state: FSMContext):
    async with state.proxy() as data: data['academy_name'] = message.text
    await states.GiveDiploma.next()
    await message.answer(text=texts.DIPLOMA_REGISTRATION_STEPS[4]) 

async def giving_date_course_start(message: Message, state: FSMContext):
    async with state.proxy() as data: data['date_course_start'] = message.text
    await states.GiveDiploma.next()
    await message.answer(text=texts.DIPLOMA_REGISTRATION_STEPS[5])

async def giving_date_course_end(message: Message, state: FSMContext):
    async with state.proxy() as data: data['date_course_end'] = message.text
    await states.GiveDiploma.next()
    await message.answer(text=texts.DIPLOMA_REGISTRATION_STEPS[6])

async def giving_average_grade(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['average_grade'] = message.text
        try: await bot.send_message(data["user_id"], texts.DIPLOMA_WAS_GIVEN)
        except (CantInitiateConversation, CantTalkWithBots): pass
        await DB.save_diploma(data=data.as_dict())
    await message.answer(text="<b>Диплом видан.</b>")
    await state.finish()

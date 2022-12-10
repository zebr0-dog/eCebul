from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.utils.exceptions import CantInitiateConversation, CantTalkWithBots
from aiogram.dispatcher import FSMContext

import texts
import buttons
import states
import variables
from main import bot, LOG_CHANNEL, DB

async def registration_msg(message: Message):
    await message.answer(text=texts.FORM_TEXT)
    await states.Register.pass_application.set()

async def registration(message: Message, state: FSMContext):
    username = message.from_user.username
    user_id = message.chat.id
    text = message.text
    await state.finish()
    await bot.send_message(
        LOG_CHANNEL,
        texts.NEW_REQUEST.format(
            text=text,
            id=user_id,
            username=username
        ))
    await message.answer(text="<b>☺️ Успіх! Твої дані надіслано, чекай відповідь!</b>")

async def application_was_cancelled(msg: Message):
    command, target, *b = msg.text.split()
    await bot.send_message(int(target), "Вам відмовлено в громадянстві")
    await msg.answer("OK")

async def give(message: Message):
    await states.GivePassport.id_pass.set()
    await message.answer(text=texts.FIRST_STEP)

async def giving_id(message: Message, state: FSMContext):
    await state.update_data(id=message.text)
    await states.GivePassport.next()
    await message.answer(text=texts.SECOND_STEP)

async def giving_name(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await states.GivePassport.next()
    await message.answer(text=texts.THIRD_STEP)

async def giving_surname(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['surname'] = message.text
    await states.GivePassport.next()
    await message.answer(
        text=texts.FOURTH_STEP,
        reply_markup=buttons.sex_keyboard()
    )

async def giving_sex(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['sex'] = variables.SEX_REVERSED[message.text]
    await states.GivePassport.next()
    await message.answer(
        text=texts.FIVETH_STEP,
        reply_markup=ReplyKeyboardRemove()
    ) 

async def giving_username(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['tag'] = message.text
    await message.answer(text=texts.SIXTH_STEP)
    await states.GivePassport.next()

async def giving_balance(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['balance'] = message.text
    await message.answer(text="✅<b> Баланс встановлено!</b>")
    await message.answer(text="ℹ️ <b>Статус громадянства:\n\nНатисніть кнопку</b>", reply_markup=buttons.status_keyboard())
    await states.GivePassport.next()

async def giving_info(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['info'] = variables.STATUSES[message.text]
    await message.answer(
        text="<b>OK!</b>",
        reply_markup=ReplyKeyboardRemove()
    )
    await message.answer(
        text="<b>Інформація про роботу:\n\nНатисніть кнопку</b>",
        reply_markup=buttons.job_keyboard()
    )
    await states.GivePassport.next()

async def giving_job(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['job'] = variables.JOBS[message.text]
        print(data["id"])
        try:
            await bot.send_message(data["id"], texts.PASSPORT_WAS_GIVEN)
        except (CantInitiateConversation, CantTalkWithBots):
            pass
        await DB.save_passport(data=data.as_dict())
    await message.answer(
        text="<b> Документ створено!</b>",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.finish()

from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.utils.exceptions import CantInitiateConversation
from aiogram.dispatcher import FSMContext

import texts
import db
import buttons
import states
from main import bot

async def start(message: Message):
    await message.answer(
        text=texts.HELLO_MESSAGE,
        reply_markup=buttons.start_menu
    )

async def start_signed_up(message: Message):
    passport = await db.get_passport(id=message.from_user.id)
    name, surname, sex, tag, job, balance, info, *serv = passport
    await message.answer(texts.PASSPORT.format(
        name=name,
        surname=surname,
        sex=sex,
        id=message.from_user.id,
        job=job,
        info=info,
    ))

async def registration_msg(message: Message):
    if message.chat.id == message.from_user.id:
        await message.answer(
            text="<b>Розпочинаємо процедуру реєстрації!</b>",
            reply_markup=ReplyKeyboardRemove()
        )
        await message.answer(text=texts.FORM_TEXT)
        await states.Register.pass_application.set()

async def registration(message: Message, state: FSMContext):
    username = message.from_user.username
    user_id = message.chat.id
    text = message.text
    await state.finish()
    await bot.send_message(
        -1001542965657,
        texts.NEW_REQUEST.format(
            text=text,
            id=user_id,
            username=username
        ))
    await message.answer(text="<b>☺️ Успіх! Твої дані надіслано, чекай відповідь!</b>")

async def give(message: Message):
    await message.answer(text=texts.WARNING_ALERT)
    await states.GivePassport.id_pass.set()
    await message.answer(text=texts.FIRST_STEP)

async def citiezinship_was_cancelled(msg: Message):
    command, target, *b = msg.text.split()
    await bot.send_message(int(target), "Вам відмовлено в громадянстві")
    await msg.answer("OK")

async def cancel_giving(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply("Операція скасована", reply_markup=ReplyKeyboardRemove())

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
        reply_markup=buttons.sex_menu
    )

async def giving_sex(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['sex'] = message.text
    await states.GivePassport.next()
    await message.answer(
        text=texts.FIVETH_STEP,
        reply_markup=ReplyKeyboardRemove()
    )

async def giving_username(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['tag'] = message.text
    await message.answer(text=texts.SIXTH_STEP, reply_markup=buttons.balance_reg)
    await states.GivePassport.next()

async def giving_balance(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['balance'] = message.text
    await message.answer(
        text="✅<b> Баланс встановлено!</b>",
        reply_markup=ReplyKeyboardRemove())
    await message.answer(
        text="ℹ️ <b>Додаткова інформація:\n\nНатисніть кнопку</b>",
        reply_markup=buttons.change_info
    )
    await states.GivePassport.next()

async def giving_info(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['info'] = message.text
    await message.answer(
        text="<b> Доповнено!</b>",
        reply_markup=ReplyKeyboardRemove()
    )
    await message.answer(
        text="<b>Інформація про роботу:\n\nНатисніть кнопку</b>",
        reply_markup=buttons.job_reg
    )
    await states.GivePassport.next()

async def giving_job(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['robota'] = message.text
    await message.answer(
        text="<b> Документ створено!</b>",
        reply_markup=ReplyKeyboardRemove()
    )
    await message.answer(
        text="<b> Натисніть кнопку щоб затвердити:</b>",
        reply_markup=buttons.complete
    )
    await states.GivePassport.create_pass_log.set()

async def registration_logname(message: Message, state: FSMContext):
    async with state.proxy() as data:
        id = data.get("id")
        try:
            await bot.send_message(id, texts.PASSPORT_WAS_GIVEN)
        except CantInitiateConversation:
            pass
        await db.save_passport(data=data)
    await message.answer(
        text="<b> Видача документа затверджена, дякую!</b>",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.finish()
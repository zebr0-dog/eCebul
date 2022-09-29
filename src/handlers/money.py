from curses.ascii import FS
from aiogram.types import Message
from aiogram.dispatcher import FSMContext

import states
import texts
import db

from main import bot, LOG_CHANNEL

async def balance(msg: Message):
    passport = await db.get_passport(msg.from_user.id)
    if passport:
        name, surname, sex, username, job, balance, info, active = passport
        await msg.answer(texts.BANK_ACCOUNT.format(
            username=msg.from_user.username,
            balance=balance
        ),
        disable_web_page_preview=True
        )

async def pay_by_id(msg: Message):
    await msg.answer("Введіть ID отримувача")
    await states.Pay.id.set()

async def get_id(msg: Message, state: FSMContext):
    await state.update_data(id=msg.text)
    await msg.answer("Введіть суму переводу")
    await states.Pay.sum.set()

async def get_sum(msg: Message, state: FSMContext):
    data = await state.get_data()
    target = int(data.get("id"))
    res = await db.add_or_take_money(
        id=target,
        sum=msg.text,
        operation="+"
    )
    if res == 0:
        await db.add_or_take_money(
            id=msg.from_user.id,
            sum=msg.text,
            operation="-"
        )
        await msg.answer(f"Ви переказали {msg.text} чорних злотих.")
        await bot.send_message(
            target,
            f"Вам переказали {msg.text} чорних злотих."
        )
        await bot.send_message(LOG_CHANNEL, f'Користувач @{msg.from_user.username} перевів користувачу ID:{target} {msg.text} чорних злотих')
    await state.finish()

async def pay_by_reply(msg: Message):
    cmd, sum, *a = msg.text.split(" ", 1)
    res = await db.add_or_take_money(
        id=msg.from_user.id,
        sum=sum,
        operation="-"
    )
    if res == 0:
        await db.add_or_take_money(
            id=msg.reply_to_message.from_user.id,
            sum=sum,
            operation="+"
        )
        await msg.reply("Переказ виконано")
        await bot.send_message(LOG_CHANNEL, f'Користувач @{msg.from_user.username} переказав користувачу @{msg.reply_to_message.from_user.username} {sum} чорних злотих')
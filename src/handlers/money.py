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
    target = str(msg.text)
    if len(target) >= 2:
        if target[1] == ':':
            target = int(target[0])
            res = await db.get_fund_by_id(int(target))
        else:
            res = False
    else: res = False
    
    if not res:
        await msg.answer('Неіснуючі реквізити')
        await state.finish()
    await msg.answer("Введіть суму переводу")
    await states.Pay.sum.set()

async def get_sum(msg: Message, state: FSMContext):
    data = await state.get_data()
    if not '-' in msg.text:
        target = str(data.get("id"))
        full_target = target
        if target[0] == 'Ц' and target[-1] == 'Р':       
            target = target[1:]
            target = int(target[:-1])
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
                user_from = await db.get_passport(id=msg.from_user.id)
                user_to = await db.get_passport(id=target)
                await msg.answer(f"Ви переказали {msg.text} чорних злотих.")
                await bot.send_message(
                    target,
                    f"Громадянин {user_from[0]} {user_from[1]} переказав вам {msg.text} чорних злотих."
                )
                await bot.send_message(LOG_CHANNEL, f'Користувач @{msg.from_user.username} перевів користувачу {user_to[3]} {msg.text} чорних злотих')
        elif target[1] == ':':
            target = int(target[0])
            fund = await db.get_fund_by_id(target)
            if fund:
                res = await db.replenish_fund_money(target, msg.text, msg.from_user.id, True)
                if res:
                    await msg.answer(f"Ви переказали {msg.text} чорних злотих на рахунок фонду\n#️⃣{full_target}")
                    await bot.send_message(LOG_CHANNEL, f'Користувач @{msg.from_user.username} перевів на рахунок фонду #️⃣{full_target} {msg.text} чорних злотих')
                else:
                    await msg.answer('Неіснуючі реквізити')
    else:
        await msg.answer('Соси хуй, багоюзер')
    await state.finish()

async def pay_by_reply(msg: Message):
    if msg.from_user.id == msg.reply_to_message.from_user.id:
        return
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
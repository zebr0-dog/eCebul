from unicodedata import name
from aiogram.types import Message
from aiogram.dispatcher import FSMContext

import db
import texts
import states
from main import bot

async def create_fund(message: Message):
    await message.answer('Починаємо створення фонду. Вкажіть ID власника фонду')
    await states.CreateFund.fund_owner_id.set()
    
async def get_fund_owner_id(msg: Message, state: FSMContext):
    await state.update_data(fund_owner_id=msg.text)
    await msg.answer("Вкажіть назву фонду")
    await states.CreateFund.fund_name.set()
    
async def get_fund_name(msg: Message, state: FSMContext):
    await state.update_data(fund_name=msg.text)
    await msg.answer("Вкажіть баланс фонду")
    await states.CreateFund.fund_balance.set()
    
async def get_fund_balance(msg: Message, state: FSMContext):
    await state.update_data(fund_balance=msg.text)
    data = await state.get_data()
    owner_id = int(data.get("fund_owner_id"))  # type: ignore
    name = str(data.get("fund_name"))
    await db.fund.FundDB().create_fund(
        owner_id = owner_id,
        balance = int(float(data.get("fund_balance"))),  # type: ignore
        name = name
    )
    await msg.answer("Створення фонду завершено. Дякуємо")
    await bot.send_message(owner_id, f'Вас було заявлено власником фонду {name}')
    await state.finish()
    

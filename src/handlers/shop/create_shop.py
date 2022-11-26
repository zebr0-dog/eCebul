from aiogram.types import Message
from aiogram.dispatcher import FSMContext

from asyncio import sleep
from db import create_shop as c
from db import id_shop, get_fund_by_id
from states import CreateShop
from main import bot



async def create_shop(message: Message):
    await message.answer("Доброго дня, починаємо створення магазину. Обробляю потрібну інформацію...")
    await sleep(2)
    await message.answer("Напишіть ID власника магазину")
    await CreateShop.shop_owner_id.set()

async def get_owner_id(message: Message, state: FSMContext):
    await state.update_data(shop_owner_id=message.text)
    await message.answer("Напишіть назву магазину")
    await CreateShop.shop_title.set()

async def get_title(message: Message, state: FSMContext):
    await state.update_data(shop_title=message.text)
    await message.answer("Напишіть коротке вітальне повідомлення для покупця")
    await CreateShop.default_message.set()
    
async def get_message(message: Message, state: FSMContext):
    await state.update_data(default_message=message.text)
    await message.answer("Дякую, очікуйте кілька секунд")
    await sleep(2)
    await message.answer("Напишіть мені Фонд магазину, це обов'язково")
    await CreateShop.shop_fund.set()

async def get_fund(message: Message, state: FSMContext):
    fund = await get_fund_by_id(fund_id=int(message.text))
    if fund:
        await state.update_data(shop_fund=int(message.text))
        data = await state.get_data()
        owner_id = int(data.get("shop_owner_id"))
        id = await id_shop(title = str(data.get("shop_title")))
        title = data.get("shop_title")
        await c(
            title = data.get("shop_title"),
            owner_id = owner_id,
            fund_id = data.get("shop_fund"),
            default_message = data.get("default_message"),
        )
        await message.answer("Магазин створено")
        await sleep(2)
        await bot.send_message(owner_id, f"На ваше ім'я зареєстровано магазин {title}, ID - {id}")
        await state.finish()
    
    
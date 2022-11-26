from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher import FSMContext

from asyncio import sleep
from states import CreateItem
from db import my_shop, id_shop, is_my_shop, create_item, replenish_fund_money
from main import bot, LOG_CHANNEL




async def createitem(message: Message):
    my_shops = await my_shop(owner_id = message.from_user.id)
    if my_shops:
        text = "<strong>Магазини у Республіці</strong>\n<em>Вітаємо на Головній Площі!\n</em>"
        shops = ReplyKeyboardMarkup(resize_keyboard=True)
        for shop in my_shops:
            id = await id_shop(title=shop[0])
            n = KeyboardButton(text =shop[0] + " " +'ID: ' + str(id[0]))
            shops.add(n)
        await message.answer("Вкажіть ID магазину у який завозимо предмети...", reply_markup = shops)
        await CreateItem.shop_id.set()
        
    else:
        text = f'Якась помилка, магазинів немає \n<em>Ви точно купили магазин?</em>'
        await message.reply(text) 
    

async def get_s_id(message: Message, state: FSMContext):
    id=message.text[-1]
    s = await is_my_shop(shop_id = int(id), sender_id = message.from_user.id)
    if s == True:
        await message.answer(message.text[-1])
        await state.update_data(shop_id=message.text[-1])
        await message.answer("Напишіть назву предмету")
        await CreateItem.item_name.set()
    else: 
        await message.answer("Вкажіть ID магазину у який завозимо предмети і який вам належить!", reply_markup = shops)
        await CreateItem.shop_id.set()

async def get_name(message: Message, state: FSMContext):
    await state.update_data(item_name=message.text)
    await message.answer("Напишіть кількість завезених товарів")
    await CreateItem.item_count.set()
    
async def get_count(message: Message, state: FSMContext):
    x = isinstance(int(message.text), int)
    if x == True:
        await state.update_data(item_count=message.text)
        await message.answer("Напишіть короткий опис до товару:")
        await CreateItem.description.set()
    else:
        await message.answer("Не бавтеся! Напишіть кількість товарів числом!")
        await CreateItem.item_count.set()
        
async def get_desc(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer("Ціна за 1 штуку:")
    await CreateItem.item_cost.set()

async def get_cost(message: Message, state: FSMContext):
    x = isinstance(int(message.text), int)
    if x == True:
        await state.update_data(item_cost=message.text)
        await message.answer("Напишіть статус вашого товару товару:")
        await CreateItem.item_status.set()
    else:
        await message.answer("Не бавтеся! Напишіть ціну числом!")
        await CreateItem.item_cost.set()

async def get_status(message: Message, state: FSMContext):
    await state.update_data(item_status=message.text)
    data = await state.get_data()
    await message.answer("Дякуємо, обробка")
    amount = int(data.get("item_cost")) * int(data.get("item_count")) * 0.75
    res = await replenish_fund_money(1, int(amount), message.from_user.id)
    if res:
        if res[0] == 0:
            await message.reply(f'Успішно додано до держбюджету {int(amount)} чорних злотих')
            await bot.send_message(
                    LOG_CHANNEL,
                    f'Користувач @{message.from_user.username} додав до держбюджету {amount} чорних злотих'
            )
            await state.update_data(item_status=message.text)

            await create_item(
                s_id = data.get("shop_id"),
                name = data.get("item_name"),
                count = data.get("item_count"),
                desc = data.get("description"),
                cost = data.get("item_cost"),
                status = data.get("item_status"),
            )
            await message.answer("Вітаємо, ви завезли товари в магазини")
            await state.finish()
        elif res[0] == 1:
            await message.reply('У вас не достатньо коштів щоб оплатити завезення товарів')
            await state.finish()
    
    
    

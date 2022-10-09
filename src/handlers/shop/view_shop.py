from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from db import list_shop, title_shop


async def shop_view(message: Message):
    shops = await list_shop()
    if shops:
        text = "<strong>Магазини у Республіці</strong>\n<em>Вітаємо на Головній Площі!\n</em>"
        shop = InlineKeyboardMarkup()
        for i in range(1, len(shops) + 1):
            shop_title = await title_shop(id = i)
            n = InlineKeyboardButton(shop_title[0][0], callback_data=shop_title[0][0])
            shop.add(n)
        await message.reply(text, reply_markup = shop)
    else:
        text = f'Якась помилка, магазинів немає \n<em>Все винесли, навіть перекотиполе не залишили, тварини</em>'
        await message.reply(text) 
  
  
async def my_shops(message: Message):
    pass
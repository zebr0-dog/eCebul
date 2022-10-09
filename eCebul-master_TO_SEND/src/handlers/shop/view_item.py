from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from db import list_item, id_shop, bought
from . import callbacks
async def item_view(message: Message, bot, title):
    id= await id_shop(title = title)
    items = await list_item(shopid = id[0])
    if items:
        text = "<strong>Речі на стелажах</strong>\n<em>Натисніть щоб дізнатися більше\n</em>"
        items_ = InlineKeyboardMarkup()
        for i in range(0, len(items)):
            n = InlineKeyboardButton(items[i][0], callback_data=i)
            items_.add(n)
        await bot.send_message(message.from_user.id, text, reply_markup = items_)
    else:
        text = f'Речі в магазин ще не завезли \n<em>Перекотиполеее</em>'
        await bot.send_message(message.from_user.id, text) 

async def my_items(message: Message):
    b = bought(id_b = message.from_user.id)
    text = "<strong>Ваші предмети:</strong>\n"
    for item in b:
        name = item[0]
        description = item[1]
        status = item[2]
        text = text + name + ":\n <em>" + description + "</em> Статус:" + "<code>"+ status +"</code>\n"
    await message.reply(text) 
    
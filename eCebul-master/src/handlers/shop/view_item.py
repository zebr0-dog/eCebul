from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from db import list_item, id_shop, my_item


async def item_view(message: Message, bot, title):
    id= await id_shop(title = title)
    items = await list_item(shop_id = id[0])
    if items:
        text = f"<strong>Речі на стелажах</strong>\n<em>Натисніть щоб дізнатися більше\n</em>"
        items_ = InlineKeyboardMarkup()
        for item in items:
            callback = str(id[0])+item[0]
            n = InlineKeyboardButton(item[0], callback_data=callback)
            items_.add(n)
        await bot.send_message(message.from_user.id, text, reply_markup = items_)
    else:
        text = f'Речі в магазин ще не завезли \n<em>Перекотиполеее</em>'
        await bot.send_message(message.from_user.id, text) 

async def my_items(message: Message):
    items = await my_item(id = message.from_user.id)
    if items:
        text = f"<strong>Речі @{message.from_user.username}</strong>:\n\n"
        texts = []
        used =[]
        for item in items:
            texts.append(f"<strong>Назва:</strong> {item[1]}\n<strong>Опис предмету:</strong> {item[2]} \n<strong>Статус предмету:</strong> {item[3]}\n")
        for i in range(0, len(texts)):
            amount = texts.count(texts[i])
            if amount == 1:
                text = text + texts[i] + "\n\n"
            else:
                if texts[i] in used:
                    continue
                else:
                    text = text + texts[i] + f"Всього предметів: {amount}\n\n\n"
            used.append(texts[i])
        await message.reply(text)
    else:
        text = f'У вас немає предметів \n<em>Напишіть <code>!магазин</code> щоб щось купити</em>'
        await message.reply(text) 
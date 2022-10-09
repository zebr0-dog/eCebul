from main import bot
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from db import list_shop, title_shop, def_msg, item, add_or_take_money, buy_item
from . import view_item
 
async def shopes(cb: CallbackQuery):
    data = cb.data
    shops = await list_shop()
    for i in range(1, len(shops) + 1):
        shop_title = await title_shop(id = i)
        if data == shop_title[0][0]:
            text = await def_msg(title = shop_title[0][0])
            await bot.send_message(cb.from_user.id, text[0])
            await bot.send_message(cb.message.chat.id, "<em>Магазин у приватних повідомленнях</em>") 
            await view_item.item_view(cb, bot, shop_title[0][0])
            await cb.message.delete()
    return(data)


async def itemes(cb: CallbackQuery):
    c = await shopes(cb)
    for i in range(0, 5):
        if c == i:
            item = await item(id = i)
            item = item[0]
            text = "<em>Назва:</em> " + item[0] + "\n" +  "<em>Опис:</em> " + item[4] + "\n" + "<em>Статус предмету:</em> " + item[3] + "\n" + "<em>Ціна:</em> " + item[2] + "\n"
            item_mark = InlineKeyboardMarkup()
            buy = InlineKeyboardButton('Купити', callback_data="buy"+str(i))
            await bot.send_message(cb.from_user.id, text, reply_markup = item_mark)
            await cb.message.delete()
        elif c[:3] == "buy":
            cost = c[3:]
            res = await add_or_take_money(id=msg.from_user.id, sum=cost, operation="-")
            if res == 0 or 3:
                await buy_item(id_item=i, id_buyer=cb.from_user.id, name = item[0], desc=item[4], status=item[3])
                await bot.send_message(cb.from_user.id, 'Вітаю з покупкою')
                await cb.message.delete()
            else:
                await bot.send_message(cb.from_user.id, 'Еммм... Щось пішло не так')

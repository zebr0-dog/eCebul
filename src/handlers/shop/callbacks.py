from main import bot
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from db import list_shop, title_shop, def_msg, list_item, current_item, view_item_id, buy_item, add_or_take_money, fund_shop, replenish_fund_money
from . import view_item
 
async def shopes(cb: CallbackQuery):
    data = cb.data
    shops = await list_shop()
    if shops:
        for i in range(1, len(shops) + 1):
            shop_title = await title_shop(id = i)
            if data == shop_title[0][0]:
                text = await def_msg(title = shop_title[0][0])
                await bot.send_message(cb.from_user.id, text[0])
                await bot.send_message(cb.message.chat.id, "<em>Магазин у приватних повідомленнях</em>") 
                await cb.message.delete()
                await view_item.item_view(cb, bot, shop_title[0][0])
            else:
                items = await list_item(shop_id = i)
                if items:
                    for item in items:
                        if data == str(i)+item[0]:
                            current_id = await view_item_id(shop = i, name = item[0])
                            current = await current_item(id = current_id[0])
                            current = current[0]
                            text = "<em><strong>Назва:</strong></em> " + current[1] + "\n" +  "<em><strong>Опис:</strong></em> " + current[2] + "\n" + "<em><strong>Статус предмету:</strong></em> " + current[5] + "\n" +  "<em>Залишилося " + str(current[0]) + " предметів у цьому магазині</em>\n" +"<em><strong>Ціна:</strong></em> " + str(current[4]) + "\n"
                            markup = InlineKeyboardMarkup()
                            btn = InlineKeyboardButton("Купити цей предмет", callback_data='buy'+str(i)+item[0])
                            markup.add(btn)
                            await bot.send_message(cb.from_user.id, text, reply_markup = markup)
                            await cb.message.delete()
                        elif data == 'buy'+str(i)+item[0]:
                            current_id = await view_item_id(shop = i, name = item[0])
                            current = await current_item(id = current_id[0])
                            current = current[0]
                            if current[0] <= 0:
                                await bot.answer_callback_query(cb.id, text=f"❗ПОМИЛКА❗\nПокупку відхилено. У магазині не залишилося товару\nВибачте за тимчасові незручності", show_alert=True)

                            else:
                                fshop = await fund_shop(id =i)
                                res = await replenish_fund_money(fshop[0][0], current[4], cb.from_user.id)
                                if res:
                                    if res[0] == 0:
                                        count = current[0]-1
                                        print(count)
                                        await buy_item(user_id = cb.from_user.id, item_id = current_id[0], name = current[1], description = current[2], status = current[5], count = count)
                                        await bot.answer_callback_query(cb.id, text=f"Вітаю з покупкою.\nВи придбали {current[1]} за {current[4]} чорних злотих!", show_alert=True)
                                        await cb.message.delete()
                                    elif res[0] == 1:
                                        await bot.answer_callback_query(cb.id, text="❗ПОМИЛКА❗\nПокупку відхилено. Недостатньо коштів\n Вибачте за тимчасові незручності", show_alert=True)
                                    else:
                                        await bot.answer_callback_query(cb.id, text="❗ПОМИЛКА❗\nПокупку відхилено. Невідома помилка\n Вибачте за тимчасові незручності", show_alert=True)
                        else:
                            continue
                else:
                    continue
    else:
        await bot.send_message(cb.message.chat.id,"Якийсь баг, розбираюся") 
        await cb.message.delete()
    

    

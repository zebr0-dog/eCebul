from aiogram.types import Message

import db
import json

from main import bot, LOG_CHANNEL

async def check_admin_rank(user_id: int):
    user_data = await db.get_admin(id=user_id)
    max_value = max(user_data.values())
    rang = ...
    if max_value >= 3:
        rang = 3
    else:
        rang = False
    return rang

async def add_manager(message: Message):
    cmd, fund_id, user_id, *all = message.text.split()
    fund_id = fund_id[0]
    fund = await db.get_fund_by_id(fund_id=fund_id)
    user_admin_rank = await check_admin_rank(user_id=message.from_user.id)
    if int(message.from_user.id) == int(json.loads(fund[0][4])[0]) or user_admin_rank:
        res = await db.add_user_to_fund(fund_id=fund_id, user_id=user_id)
    else:
        res = False
        await message.answer('Помилка, ви не маєте достатнього рівня прав, або не є власником фонду')
    if res:
        await message.answer('Користувача успішно додано до фонду')
        
        await bot.send_message(user_id, f'Вас додано до персоналу фонду {json.loads(fund[0][3])}')
        
        
async def delete_manager(message: Message):
    cmd, fund_id, user_id, *all = message.text.split()
    fund_id = fund_id[0]
    fund = await db.get_fund_by_id(fund_id=fund_id)
    user_admin_rank = await check_admin_rank(user_id=message.from_user.id)
    if int(message.from_user.id) == int(json.loads(fund[0][4])[0]) or user_admin_rank:
        res = await db.delete_user_from_fund(fund_id=fund_id, user_id=user_id)
    else:
        res = False
        await message.answer('Помилка, ви не маєте достатнього рівня прав, або не є власником фонду')
    if res:
        await message.answer('Користувача успішно видалено з фонду')
        await bot.send_message(user_id, f'Вас видалено з персоналу фонду {json.loads(fund[0][3])}')
    else:
        await message.answer('Ви не можете видалити власника з фонду')
        
async def withdraw_money(message: Message):
    cmd, fund_id, amount, *all = message.text.split()
    fund_id = fund_id[0]
    res = await db.withdraw_fund_money(fund_id, amount)
    if res:
        if res[0] == 0:
            if int(fund_id) == 1:
                await message.reply(f'З держбюджету списано {amount} чорних злотих')
                await bot.send_message(
                        LOG_CHANNEL,
                        f'Користувач @{message.from_user.username} списав з держбюджету {amount} чорних злотих'
                )
            else:   
                await message.reply(f'З фонду {res[1]} успішно списано {amount} чорних злотих')
                await bot.send_message(
                        LOG_CHANNEL,
                        f'Користувач @{message.from_user.username} списав з рахунку фонду "{res[1]}" {amount} чорних злотих'
                )
                
async def take_money(message: Message):
    cmd, fund_id, amount, *all = message.text.split()
    fund_id = fund_id[0]
    user_admin_rank = await check_admin_rank(message.from_user.id)
    fund = await db.get_fund_by_id(fund_id=fund_id)
    if int(message.from_user.id) in json.loads(fund[0][4]):
        res = await db.take_fund_money(fund_id, amount, message.from_user.id)
        if res:
            if res[0] == 0:
                if int(fund_id) == 1:
                    await message.reply(f'З держбюджету знято {amount} чорних злотих')
                    await bot.send_message(
                            LOG_CHANNEL,
                            f'Користувач @{message.from_user.username} зняв з держбюджету {amount} чорних злотих'
                    )
                else:   
                    await message.reply(f'З фонду {res[1]} успішно знято {amount} чорних злотих')
                    await bot.send_message(
                            LOG_CHANNEL,
                            f'Користувач @{message.from_user.username} зняв з рахунку фонду "{res[1]}" {amount} чорних злотих'
                    )

async def replenish_fund(message: Message):
    cmd, fund_id, amount, *all = message.text.split()
    fund_id = fund_id[0]
    res = await db.replenish_fund_money(fund_id, amount, message.from_user.id)
    if res:
        if res[0] == 0:
            if int(fund_id) == 1:
                await message.reply(f'Успішно додано до держбюджету {amount} чорних злотих')
                await bot.send_message(
                        LOG_CHANNEL,
                        f'Користувач @{message.from_user.username} додав до держбюджету {amount} чорних злотих'
                )
            else:
                await message.reply(f'Рахунок фонду {res[1]} успішно поповнено на {amount} чорних злотих')
                await bot.send_message(
                        LOG_CHANNEL,
                        f'Користувач @{message.from_user.username} поповнив рахунок фонду "{res[1]}" на {amount} чорних злотих'
                )
        elif res[0] == 1:
            await message.reply('У вас не достатньо коштів')

            
            

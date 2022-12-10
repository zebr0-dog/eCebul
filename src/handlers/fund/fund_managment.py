from aiogram.types import Message

import json

from main import bot, DB, LOG_CHANNEL

async def add_manager(message: Message):
    cmd, fund_id, user_id, *bloat = message.text.split()
    fund = await DB.get_fund(fund_id=int(fund_id))
    if fund:
        await DB.add_user_to_fund(fund_id=fund.id, user_id=int(user_id), can_add_personal=False, can_withdraw=True)
        await message.answer('Користувача успішно додано до фонду')
        await bot.send_message(int(user_id), f'Вас додано до персоналу фонду {fund.name}')
        
async def delete_manager(message: Message):
    cmd, fund_id, user_id, *all = message.text.split()
    fund = await DB.get_fund(fund_id=int(fund_id))
    if fund:
        res = await DB.delete_user_from_fund(fund_id=int(fund_id), user_id=int(user_id))
        await message.answer('Користувача успішно видалено з фонду')
        await bot.send_message(int(user_id), f'Вас видалено з персоналу фонду {fund.name}')
        
async def withdraw_money(message: Message):
    cmd, fund_id, amount, *all = message.text.split()
    fund_id = fund_id.split(":")[0]
    res = await DB.withdraw_money(message.from_user.id, int(fund_id), int(amount))
    match res:
        case 1:
            await message.reply("Ви не можее зняти більше, ніж є в фонді")
        case 2:
            await message.reply("Ви не маєте права на зняття коштів з фонду")
        case 3:
            await message.reply("Фонду не існує")
        case 4:
            await message.reply("Ви не можете зняти від'ємну суму")
        case _:
            await message.reply(f'З фонду {res[1]} успішно списано {amount} чорних злотих')
            await bot.send_message(
                LOG_CHANNEL,
                f'Користувач {message.from_user.mention} списав з рахунку фонду "{res[1]}" {amount} чорних злотих'
            )

async def replenish_fund(message: Message):
    cmd, fund_id, amount, *all = message.text.split()
    fund_id = fund_id.split(":")[0]
    res = await DB.replenish_money(int(fund_id), message.from_user.id, int(amount))
    match res:
        case 1:
            await message.reply("В вас недостатньо коштів")
        case 2:
            await message.reply("Фонду не існує")
        case 3:
            await message.reply("Ви не можете зняти від'ємну суму")
        case _:
            await message.reply(f'Рахунок фонду {res[1]} успішно поповнено на {amount} чорних злотих')
            await bot.send_message(
                LOG_CHANNEL,
                f'Користувач {message.from_user.mention} поповнив рахунок фонду "{res[1]}" на {amount} чорних злотих'
            )
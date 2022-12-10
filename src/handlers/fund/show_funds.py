from aiogram.types import Message

import texts

from main import DB

async def get_funds(message: Message):
    list_of_funds = await DB.get_all_funds()
    if list_of_funds:
        text = "<b>Фонди Кавуневої Республіки</b>\n"
        for fund in list_of_funds:
            owner_passport = await DB.get_passport(id=fund.owner)
            if owner_passport:
                text = "\n".join([
                        text,
                        texts.FUND.format(
                            fund_name=fund.name,
                            fund_id=fund.id,
                            fund_owner_id=fund.owner,
                            owner_username=owner_passport.username[1::],
                            owner_name=owner_passport.name,
                            owner_surname=owner_passport.surname
                        )
                ])
        await message.reply(text)
    else:
        await message.reply('Поки фондів немає') 
        
async def get_fund(message: Message):
    command, fund_id, *all = message.text.split()
    fund_id = fund_id.split(":")[0]
    fund = await DB.get_fund(fund_id=int(fund_id))
    if fund:
        owner_passport = await DB.get_passport(id=fund.owner)
        if not owner_passport:
            return
        personal = await DB.get_personal(fund_id=fund.id)
        text = texts.FUND_DETAILED.format(
            name=fund.name,
            id=fund.id,
            owner=fund.owner,
            username=owner_passport.username,
            owner_name=owner_passport.name,
            surname=owner_passport.surname,
            balance=fund.balance
        )
        have_access = ""
        if personal:
            for id, employee in personal.items():
                user = await DB.get_passport(id=id)
                if user:
                    have_access = "".join([
                        have_access,
                        f"<a href=\"t.me/{user.username}\">{user.name} {user.surname}</a>, "
                    ])
        data = " ".join([text, have_access[:-1:]])
        await message.answer(data)
    else:
        await message.answer('<b>Такого фонду не існує!</b>')

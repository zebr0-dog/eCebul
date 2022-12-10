from aiogram.types import Message

import json

import db

async def delete_fund(msg: Message):
    cmd, fund_id, *bloat = msg.text.split()
    await db.fund.FundDB().delete_fund(fund_id=int(fund_id))
    await msg.answer("Фонд видалено")
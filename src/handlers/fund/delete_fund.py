from aiogram.types import Message

import json

import db

async def delete_fund(msg: Message):
    cmd, fund_id, *bloat = msg.text.split()
    await db.delete_fund(fund_id=fund_id)
    await msg.answer("Фонд видалено")
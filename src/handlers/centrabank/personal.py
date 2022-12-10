from aiogram.types import Message

from main import DB

async def add_personal(msg: Message):
    cmd, id = msg.text.split()
    await DB.add_personal(int(id))
    await msg.reply("Ви успішно найняли людину на роботу в Центральний Банк")

async def delete_personal(msg: Message):
    cmd, id = msg.text.split()
    await DB.delete_personal(int(id))
    await msg.reply("Ви звільнили працівника")

async def change_head(msg: Message):
    cmd, id = msg.text.split()
    await DB.change_head(int(id))
    await msg.reply("Ви успішно переназначили Голову Центрального Банку")
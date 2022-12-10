from aiogram.types import Message

from main import DB

async def add_money(msg: Message):
    cmd, amount = msg.text.split()
    if not (await DB.emission(int(amount), "+")):
        await msg.reply(f"У державний бюджет надруковано {amount} Чорних Злотих")
        return
    await msg.reply("Некоректна сума")

async def delete_money(msg: Message):
    cmd, amount = msg.text.split()
    if not (await DB.emission(int(amount), "-")):
        await msg.reply(f"З державного бюджеу списано {amount} Чорних Злотих")
        return
    await msg.reply("Некоректна сума")

async def give_from_cb(msg: Message):
    cmd, id, amount = msg.text.split()
    if (await DB.give_from_cb(int(amount), int(id))):
        await msg.reply("Ви успішно видали гроші з Державного Бюджету")
    else: await msg.reply("Помилка. Можливо, в Державному Бюджеті недостатньо коштів")
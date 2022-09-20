from aiogram.types import Message

import db
import texts

async def show_pass(message: Message):
    passport = await db.get_passport(id=message.from_user.id)
    if passport:
        name, surname, sex, tag, job, balance, info, *serv = passport
        await message.answer(texts.PASSPORT.format(
            name=name,
            surname=surname,
            sex=sex,
            username=tag[1::],
            job=job,
            info=info,
        ),
        disable_web_page_preview=True
        )
    else:
        await message.answer(texts.PASSPORT_DO_NOT_EXIST)

async def show_pass_admin(message: Message):
    target_id = message.reply_to_message.from_user.id
    passport = await db.get_passport(target_id)
    if passport is None:
        await message.answer(texts.PASSPORT_DO_NOT_EXIST)
    else:
        name, surname, sex, tag, job, balance, info, *a = passport
        await message.answer(texts.PASSPORT.format(
            name=name,
            surname=surname,
            sex=sex,
            username=tag[1::],
            job=job,
            info=info,
            balance=balance
        ),
        disable_web_page_preview=True
        )
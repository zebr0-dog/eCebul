from pyexpat.errors import messages
from aiogram.types import Message

import db
import texts

async def show_pass(message: Message):
    passport = await db.get_passport(id=message.from_user.id)
    if passport:
        name, surname, sex, tag, job, balance, info, emoji, partner, *serv = passport
        if partner != 0:
            _partner_profile = await db.get_passport(partner)
            partner = " ".join([_partner_profile[0], _partner_profile[1]])
        else:
            partner = "Холостяк"
        await message.answer(texts.PASSPORT.format(
            name=name,
            surname=surname,
            sex=sex,
            username=tag[1::],
            job=job,
            info=info,
            id=message.from_user.id,
            emoji=emoji,
            partner=partner
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
        name, surname, sex, tag, job, balance, info, emoji, partner, *serv = passport
        if partner != 0:
            _partner_profile = await db.get_passport(partner)
            partner = " ".join([_partner_profile[0], _partner_profile[1]])
        else:
            partner = "Холостяк"
        await message.answer(texts.PASSPORT.format(
            name=name,
            surname=surname,
            sex=sex,
            username=tag[1::],
            job=job,
            info=info,
            id=message.reply_to_message.from_user.id,
            emoji=emoji,
            partner=partner
        ),
        disable_web_page_preview=True
        )

async def find_pass_admin(message: Message):
    target_username = '@' + str(message.text).split('@')[1]
    passport = await db.get_passport_from_username(target_username)
    if passport is None:  
        await message.answer(texts.PASSPORT_DO_NOT_EXIST)
    else:
        name, surname, user_id, sex, job, balance, info, emoji, partner, *serv = passport
        if partner != 0:
            _partner_profile = await db.get_passport(partner)
            partner = " ".join([_partner_profile[0], _partner_profile[1]])
        else:
            partner = "Холостяк"
        await message.answer(texts.PASSPORT.format(
            name=name,
            surname=surname,
            sex=sex,
            username=target_username,
            job=job,
            info=info,
            id=user_id,
            emoji=emoji,
            partner=partner
        ),
        disable_web_page_preview=True
        )
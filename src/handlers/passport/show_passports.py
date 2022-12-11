from pyexpat.errors import messages
from aiogram.types import Message
from datetime import date

import texts
import variables

from main import DB

async def show_pass(message: Message):
    passport = await DB.get_passport(id=message.from_user.id)
    if passport:
        if passport.partner != 0:
            partner_passport = await DB.get_passport(passport.partner)
            if partner_passport:
                partner = " ".join([partner_passport.name, partner_passport.surname])
            else:
                partner = "Вдовець"
        else:
            partner = "Холостяк"
        await message.answer(texts.PASSPORT.format(
            name=passport.name,
            surname=passport.surname,
            sex=variables.SEX[passport.sex],
            username=passport.username[1::],
            job=variables.JOBS_REVERSED[passport.job],
            info=variables.STATUSES_REVERSED[passport.status],
            id=passport.id,
            emoji=passport.emoji,
            partner=partner,
            birthdate=date.fromisoformat(passport.birthdate).strftime("%d.%m.%Y"),
            yearsold=date.today().year - date.fromisoformat(passport.birthdate).year
        ))
    else:
        await message.answer(texts.PASSPORT_DO_NOT_EXIST)

async def show_pass_admin(message: Message):
    target_id = message.reply_to_message.from_user.id
    passport = await DB.get_passport(id=target_id)
    if passport:
        if passport.partner != 0:
            partner_passport = await DB.get_passport(passport.partner)
            if partner_passport:
                partner = " ".join([partner_passport.name, partner_passport.surname])
            else:
                partner = "Вдовець"
        else:
            partner = "Холостяк"
        await message.answer(texts.PASSPORT.format(
            name=passport.name,
            surname=passport.surname,
            sex=variables.SEX[passport.sex],
            username=passport.username[1::],
            job=variables.JOBS_REVERSED[passport.job],
            info=variables.STATUSES_REVERSED[passport.status],
            id=passport.id,
            emoji=passport.emoji,
            partner=partner,
            birthdate=date.fromisoformat(passport.birthdate).strftime("%d.%m.%Y"),
            yearsold=int(date.today.strftime("%Y"))-int(date.fromisoformat(passport.birthdate).strftime("%Y"))
        ))
    else:
        await message.answer(texts.PASSPORT_DO_NOT_EXIST)

async def find_pass_admin(message: Message):
    target_username = '@' + str(message.text).split('@')[1]
    passport = await DB.get_passport(username=target_username)
    if passport:
        if passport.partner != 0:
            partner_passport = await DB.get_passport(passport.partner)
            if partner_passport:
                partner = " ".join([partner_passport.name, partner_passport.surname])
            else:
                partner = "Вдовець"
        else:
            partner = "Холостяк"
        await message.answer(texts.PASSPORT.format(
            name=passport.name,
            surname=passport.surname,
            sex=variables.SEX[passport.sex],
            username=passport.username[1::],
            job=variables.JOBS_REVERSED[passport.job],
            info=variables.STATUSES_REVERSED[passport.status],
            id=passport.id,
            emoji=passport.emoji,
            partner=partner,
            birthdate=date.fromisoformat(passport.birthdate).strftime("%d.%m.%Y"),
            yearsold=int(date.today.strftime("%Y"))-int(date.fromisoformat(passport.birthdate).strftime("%Y"))
        ))
    else:
        await message.answer(texts.PASSPORT_DO_NOT_EXIST)

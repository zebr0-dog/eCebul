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
            if partner_passport: partner = " ".join([partner_passport.name, partner_passport.surname])
            else: partner = "Вдовець"
        else: partner = "Холостяк"
        if passport.is_citizen in ['', None, 'None'] or passport.is_citizen: passport.is_citizen = 1
        text = texts.PASSPORT.format(
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
            yearsold=(date.today() - date.fromisoformat(passport.birthdate)).days // 365,
            is_citizen=variables.CITIZENS[passport.is_citizen]
        )
        if passport.passport_photo not in ["", None, "None"]: await message.answer_photo(photo=passport.passport_photo, caption=text)
        else: await message.answer(text)
    else:
        await message.answer(texts.PASSPORT_DO_NOT_EXIST)

async def show_pass_admin(message: Message):
    target_id = message.reply_to_message.from_user.id
    passport = await DB.get_passport(id=target_id)
    if passport:
        if passport.partner != 0:
            partner_passport = await DB.get_passport(passport.partner)
            if partner_passport: partner = " ".join([partner_passport.name, partner_passport.surname])
            else: partner = "Вдовець"
        else: partner = "Холостяк"
        if passport.is_citizen in ['', None, 'None'] or passport.is_citizen: passport.is_citizen = 1
        text = texts.PASSPORT.format(
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
            yearsold=(date.today() - date.fromisoformat(passport.birthdate)).days // 365,
            is_citizen=variables.CITIZENS[passport.is_citizen]
        )
        if passport.passport_photo not in ["", None, "None"]: await message.answer_photo(photo=passport.passport_photo, caption=text)
        else: await message.answer(text)
    else:
        await message.answer(texts.PASSPORT_DO_NOT_EXIST)

async def find_pass_admin(message: Message):
    target_username = '@' + str(message.text).split('@')[1]
    passport = await DB.get_passport(username=target_username)
    if passport:
        if passport.partner != 0:
            partner_passport = await DB.get_passport(passport.partner)
            if partner_passport: partner = " ".join([partner_passport.name, partner_passport.surname])
            else: partner = "Вдовець"
        else: partner = "Холостяк"
        if passport.is_citizen in ['', None, 'None'] or passport.is_citizen: passport.is_citizen = 1
        text = texts.PASSPORT.format(
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
            yearsold=(date.today() - date.fromisoformat(passport.birthdate)).days // 365,
            is_citizen=variables.CITIZENS[passport.is_citizen]
        )
        if passport.passport_photo not in ["", None, "None"]: await message.answer_photo(photo=passport.passport_photo, caption=text)
        else: await message.answer(text)
    else:
        await message.answer(texts.PASSPORT_DO_NOT_EXIST)

async def show_diplomatic_passport(message: Message):
    passport = await DB.get_passport(id=message.from_user.id)
    if passport and passport.have_diplomatic_passport:
        text = texts.DIPLOMATIC_PASSPORT.format(
            emoji=passport.emoji,
            name=passport.name,
            surname=passport.surname,
            sex=variables.SEX[passport.sex],
            id=passport.id,
            birthdate=date.fromisoformat(passport.birthdate).strftime("%d.%m.%Y"),
            years_old=(date.today() - date.fromisoformat(passport.birthdate)).days // 365
        )
        if passport.passport_photo not in ["", None, "None"]: await message.answer_photo(photo=passport.passport_photo, caption=text)
        else: await nessage.answer(text)
    else: await message.answer(texts.DIPLOMATIC_PASSPORT_DO_NOT_EXIST)

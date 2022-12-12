from aiogram.types import Message, ChatPermissions, CallbackQuery, ReplyKeyboardRemove, InlineKeyboardMarkup
from aiogram.dispatcher import FSMContext

import datetime
import random

from main import bot, DB

import texts
import buttons

async def new_member(message: Message):
    for user in message.new_chat_members:
        await bot.restrict_chat_member(
            message.chat.id,
            user.id,
            ChatPermissions(False),
            until_date=datetime.timedelta(seconds=20)
        )
        correct = random.randint(1,4)
        await message.reply(
            texts.WELCOME_CHAT_MESSAGE.format(
            chat=message.chat.title,
            id=user.id,
            name=user.full_name,
            number=correct
        ),
        reply_markup=buttons.gen_captcha_keyboard(correct, user.id)
        )

async def mute(message: Message):
    cmd, mute_time, mute_type, *comment = message.text.split(" ", 3)
    comment = " ".join(comment)
    mute_time = int(mute_time)
    if all((mute_time, mute_type, comment)):
        if mute_type in ["г", "годин", "год"]:
            await bot.restrict_chat_member(
                message.chat.id,
                message.reply_to_message.from_user.id,
                ChatPermissions(False),
                until_date=datetime.timedelta(hours=mute_time)
            )
        elif mute_type in ["х", "хвилин", "хвилини"]:
            await bot.restrict_chat_member(
                message.chat.id,
                message.reply_to_message.from_user.id,
                ChatPermissions(False),
                until_date=datetime.timedelta(minutes=mute_time)
            )
        elif mute_type in ["д", "днів", "день"]:
            await bot.restrict_chat_member(
                message.chat.id,
                message.reply_to_message.from_user.id,
                ChatPermissions(False),
                until_date=datetime.timedelta(days=mute_time)
            )
        await message.reply(texts.RESTRICT_TEXT.format(
            admin_id=message.from_user.id,
            admin_first_name=message.from_user.first_name,
            target_id=message.reply_to_message.from_user.id,
            target_first_name=message.reply_to_message.from_user.first_name,
            mute_time=mute_time,
            mute_type=mute_type,
            comment=comment
        ))

async def unmute(message: Message):
    await bot.restrict_chat_member(
        message.chat.id,
        message.reply_to_message.from_user.id,
        ChatPermissions(True, True, True, True)
    )
    await message.reply(texts.UNRESTRICT_TEXT.format(
        admin_id=message.from_user.id,
        admin_first_name=message.from_user.first_name,
        target_id=message.reply_to_message.from_user.id,
        target_first_name=message.reply_to_message.from_user.first_name
    ))

async def ban(message: Message):
    cmd, *comment = message.text.split(" ", 1)
    comment = " ".join(comment)
    await bot.kick_chat_member(
        message.chat.id,
        message.reply_to_message.from_user.id,
    )
    await message.reply(texts.BAN_TEXT.format(
        admin_id=message.from_user.id,
        admin_first_name=message.from_user.first_name,
        target_id=message.reply_to_message.from_user.id,
        target_first_name=message.reply_to_message.from_user.first_name,
        comment=comment
    ))

async def unban(message: Message):
    await bot.restrict_chat_member(
        message.chat.id,
        message.reply_to_message.from_user.id,
        ChatPermissions(True, True, True, True)
    )
    await message.reply(texts.UNBAN_TEXT.format(
        admin_id=message.from_user.id,
        admin_first_name=message.from_user.first_name,
        target_id=message.reply_to_message.from_user.id,
        target_first_name=message.reply_to_message.from_user.first_name
    ))

async def set_admin(message: Message):
    await message.answer("Оберіть права для користувача", reply_markup=buttons.permission_buttons(message.reply_to_message.from_user.id))

async def cancel_giving(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply("Операція скасована", reply_markup=ReplyKeyboardRemove())

async def check(cb: CallbackQuery):
    await cb.answer()
    data = cb.data.split("_")
    if cb.from_user.id == int(data[1]):
        if data[0] != "cap:correct":
            await bot.unban_chat_member(
                cb.message.chat.id,
                cb.from_user.id
            )
        else:
            await bot.restrict_chat_member(
                cb.message.chat.id,
                cb.from_user.id,
                ChatPermissions(True, True, True, True)
            )
        await cb.message.delete()

async def save(cb: CallbackQuery):
    await cb.answer()
    data = cb.data.split(":")
    prefix, id, *bloat = data
    indexes = {
        1: "can_mute",
        2: "can_ban",
        3: "can_pin",
        4: "can_manage_partyies",
        5: "can_manage_money",
        6: "can_give_passports",
        7: "can_promote",
        8: "can_give_diplomas",
        100: "nothiing"
    }
    markup = cb.message.reply_markup["inline_keyboard"]
    permissions = {}
    chat = 0
    for row in markup:
        for key in row:
            splited_data = key["callback_data"].split(":")
            if (index := int(splited_data[2])) == 10:
                if bool(int(splited_data[3])):
                    chat = 0
                else:
                    chat = cb.message.chat.id
            else:
                permissions[indexes.get(int(index), "")] = bool(int(splited_data[3]))
    await DB.set_admin(id=int(id), chat=chat, **permissions)
    await cb.message.edit_reply_markup(InlineKeyboardMarkup())

async def permissions(cb: CallbackQuery):
    await cb.answer()
    data = cb.data.split(":")
    prefix, id, number, active = data
    new_status = int(not bool(int(active)))
    keyboard = cb.message.reply_markup.inline_keyboard
    data = {}
    for row in keyboard:
        for key in row:
            splited_data = key["callback_data"].split(":")
            if splited_data[2] != id:
                if splited_data[3] == "1":
                    data[splited_data[2]] = "1"
    data[number] = new_status
    await cb.message.edit_reply_markup(buttons.permission_buttons(int(id), **data))

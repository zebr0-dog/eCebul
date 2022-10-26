from aiogram.types import Message, ChatPermissions, CallbackQuery

import datetime
import random

from main import bot

import texts
import db
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
    cmd, rang, *all = message.text.split()
    await db.set_admin(
        id=message.reply_to_message.from_user.id,
        rang=rang,
        chat=message.chat.id
    )
    await message.reply(f"Користувач назначений на ранг: {rang}")

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
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext

from main import bot

import db
import states
import buttons

async def party_profile(msg: Message):
    party = await db.get_party(id=msg.from_user.id)
    if party:
        name, members = party["name"], party["members"]
        text = "".join(["👥 Учасники партії ", name, "\n"])
        for member in members:
            text = "".join([text, "\n•", member])
        await msg.answer(text, reply_markup=buttons.party_manage_keyboard(party["owner"]))
    else:
        await msg.answer("Ви не є учасником партії")

async def get_id_for_add(msg: Message, state: FSMContext):
    if msg.text.isdigit():
        party = await db.get_party(msg.from_user.id)
        party_name = party["name"]
        await msg.answer("Користувачу надіслано запрошення")
        await bot.send_message(
            int(msg.text),
            f"Вас запросили до партії {party_name}. Будьте уважні, приймаючі запрошення — якщо Ви вже в партії то будете видалені з неї",
            reply_markup=buttons.dicise_party(msg.from_user.id)
        )
    else:
        await msg.answe("Ви ввели некоректний ID")
    await state.finish()

async def get_id_for_delete(msg: Message, state: FSMContext):
    await db.delete_member_from_party(int(msg.text))
    await msg.answer("Учасника видалено")
    await state.finish()

async def add_member(cb: CallbackQuery):
    await cb.answer()
    await cb.message.answer("Введіть ID користувача, якого хочете запросити")
    await states.AddMember.id.set()

async def yes(cb: CallbackQuery):
    await cb.answer()
    owner = cb.data.split("_")[1]
    await db.add_member_to_party(cb.from_user.id, int(owner))
    await cb.message.answer("Ви вступили в партію")
    await cb.message.delete()

async def no(cb: CallbackQuery):
    await cb.answer()
    await cb.message.delete()

async def delete_member(cb: CallbackQuery):
    await cb.answer()
    await cb.message.answer("Введіть ID користувача, якого хочете видалити")
    await states.DeleteMember.id.set()
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext

from main import bot, DB

import states
import buttons

async def party_profile(msg: Message):
    party = await DB.get_party_by_user(user_id=msg.from_user.id)
    print(party)
    if party:
        text = "".join(["👥 Учасники партії ", party.name, "\n"])
        members = await DB.get_members(party_id=party.id)
        if members:
            for member in members:
                text = "".join([text, "\n•", member.name, " ", member.surname])
            await msg.answer(text, reply_markup=buttons.party_manage_keyboard(party.owner == msg.from_user.id))
    else:
        await msg.answer("Ви не є учасником партії")

async def get_id_for_add(msg: Message, state: FSMContext):
    if msg.text.isdigit():
        party = await DB.get_party_by_user(msg.from_user.id)
        if party:
            await msg.answer("Користувачу надіслано запрошення")
            await bot.send_message(
                int(msg.text),
                f"Вас запросили до партії {party.name}. Будьте уважні, приймаючі запрошення — якщо Ви вже в партії то будете видалені з неї",
                reply_markup=buttons.dicise_party(msg.from_user.id)
            )
    else:
        await msg.answer("Ви ввели некоректний ID")
    await state.finish()

async def get_id_for_delete(msg: Message, state: FSMContext):
    await DB.delete_member(int(msg.text))
    await msg.answer("Учасника видалено")
    await state.finish()

async def add_member(cb: CallbackQuery):
    await cb.answer()
    await cb.message.answer("Введіть ID користувача, якого хочете запросити")
    await states.AddMember.id.set()

async def yes(cb: CallbackQuery):
    await cb.answer()
    owner = cb.data.split("_")[1]
    await DB.add_member(cb.from_user.id, int(owner))
    await cb.message.answer("Ви вступили в партію")
    await cb.message.delete()

async def no(cb: CallbackQuery):
    await cb.answer()
    await cb.message.delete()

async def delete_member(cb: CallbackQuery):
    await cb.answer()
    await cb.message.answer("Введіть ID користувача, якого хочете видалити")
    await states.DeleteMember.id.set()

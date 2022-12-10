from aiogram.types import Message
from aiogram.dispatcher import FSMContext

import texts
import states
from main import bot, DB, LOG_CHANNEL

async def reg_party(msg: Message):
    await msg.answer(texts.FORM_PARTION_TEXT)
    await states.RegisterParty.party_application.set()

async def registration(msg: Message, state: FSMContext):
    await msg.answer("Вашу заяву буде розглянуто МВС")
    await bot.send_message(LOG_CHANNEL, msg.text)
    await state.finish()

async def create_party_start(msg: Message):
    await msg.answer("Починаємо створення партії. Вкажіть ID лідера партії")
    await states.CreateParty.id.set()

async def get_id(msg: Message, state: FSMContext):
    await state.update_data(id=msg.text)
    await msg.answer("Вкажіть назву партії")
    await states.CreateParty.name.set()

async def get_name(msg: Message, state: FSMContext):
    await state.update_data(name=msg.text)
    await msg.answer("Вкажіть ID першого члена партії")
    await states.CreateParty.id_1.set()

async def get_first_tag(msg: Message, state: FSMContext):
    await state.update_data(id1=msg.text)
    await msg.answer("Вкажіть ID другого члена партії")
    await states.CreateParty.id_2.set()

async def get_second_tag(msg: Message, state: FSMContext):
    await state.update_data(id2=msg.text)
    data = await state.get_data()
    owner_id = int(data.get("id"))  # type: ignore
    result = await DB.save_party(
        owner_id,
        data.get("name"),  # type: ignore
        data.get("id1"),  # type: ignore
        data.get("id2")  # type: ignore
    )
    if result == 0:
        await msg.answer("Створення партії затверджено. Дякую.")
        await bot.send_message(owner_id, "Вашу заяву на створення партії було схвалено")
    else:
        await msg.answer("В партії має бути як мінімум 3 учасники")
    await state.finish()
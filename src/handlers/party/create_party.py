from aiogram.types import Message
from aiogram.dispatcher import FSMContext

import texts
import states
from main import bot

async def reg_party(msg: Message):
    await msg.answer(texts.FORM_PARTION_TEXT)
    await states.RegisterParty.party_application.set()

async def registration(msg: Message, state: FSMContext):
    await msg.answer("Вашу заяву буде розглянуто МВС")
    bot.send_message(-1001542965657, msg.text)
    await state.finish()

async def create_party(msg: Message):
    await msg.answer("Починаємо створення партії. Вкажіть ID лідера партії")
    await states.CreateParty.id.set()

async def get_id(msg: Message, state: FSMContext):
    await state.update_data(id=msg.text)
    await msg.answer("Вкажіть назву партії")
    await states.CreateParty.name.set()

async def get_name(msg: Message, state: FSMContext):
    await state.update_data(name=msg.text)
    await msg.answer("Вкажіть ТЕГ першого члена партії")
    await states.CreateParty.tag_1.set()

async def get_first_tag(msg: Message, state: FSMContext):
    await state.update_data(tag1=msg.text)
    await msg.answer("Вкажіть ТЕГ другого члена партії")
    await states.CreateParty.tag_2.set()

async def get_second_tag(msg: Message, state: FSMContext):
    await state.update_data(tag2=msg.text)
    data = await state.get_data()
    owner_id = int(data.get("id"))
    await msg.answer("Створення партії затверджено. Дякую.")
    await bot.send_message(owner_id, "Вашу заяву на створення партії було схвалено")
    await state.finish()
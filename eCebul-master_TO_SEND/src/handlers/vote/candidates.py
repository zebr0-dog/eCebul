from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from db import get_all_candidates, get_name


async def candidats(message: Message):
    all_c = await get_all_candidates()
    if all_c:
        text = "Кандидати на даний момент:\n"
        for candidate in all_c:
            candidate = await get_name(id = candidate)
            text = text + "<code>" + candidate[0] + " " + candidate[1] + "</code>:" + "\n" + candidate[2] + "\n"
    else:
        text = "Кандидатів немає\n <em>ХТО ЇХ СПЕР???</em>"
    await message.reply(text)
   
   
   
 #   dp.register_message_handler(
  #      handlers.vote.candidates.candidats,
   #     level_of_right=3,
    #    commands=["slaves", "кандидати"],
    #   commands_prefix="!"
    #)  Це додати в main.py
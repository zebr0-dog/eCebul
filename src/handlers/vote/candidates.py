from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from main import DB


async def candidats(message: Message):
    all_c = await DB.get_all_candidats()
    if all_c is dict:
        text = "Кандидати на даний момент:\n"
        for id, candidate in all_c.items():  # type: ignore
            text = text + "<code>" + candidate[0] + " " + candidate[1] + "</code>:" + "\n" + candidate[2] + "\n"
    else:
        text = "Кандидатів немає\n <em>ХТО ЇХ СПЕР???</em>"
    await message.reply(text)
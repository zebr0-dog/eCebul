from aiogram.types import Message
from aiogram.dispatcher.filters import BoundFilter

import db

class isPassportExist(BoundFilter):
    key = "is_passport_exist"

    def __init__(self, is_passport_exist) -> None:
        self.is_passport_exist = is_passport_exist
    async def check(self, message: Message) -> bool:
        res = await db.get_passport(message.from_user.id)
        return bool(res)

class levelOfRight(BoundFilter):
    key = "level_of_right"

    def __init__(self, level_of_right) -> None:
        self.level_of_right = level_of_right
    
    async def check(self, message: Message) -> bool:
        data = await db.get_admin(message.from_user.id)
        if data:
            rang = data.get(message.chat.id)
            if rang >= self.level_of_right:
                if rang >= 3:
                    return {"lor": rang}
        return False
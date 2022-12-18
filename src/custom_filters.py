from typing import Optional
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.filters import BoundFilter

from main import DB

class PassportExist(BoundFilter):
    key = "passport_exist"
    def __init__(self, passport_exist: bool) -> None:
        pass

    async def check(self, message: Message) -> bool:
        res = await DB.get_passport(message.from_user.id)
        return bool(res)

class CheckPermissions(BoundFilter):
    key = "need_permission"
    def __init__(self, need_permission) -> None:
        self.need_permission = need_permission
    
    async def check(self, message: Message) -> bool:
        admin = await DB.get_admin(message.from_user.id)
        if admin:
            frick = {
                "can_mute": admin.can_mute,
                "can_ban": admin.can_ban,
                "can_pin": admin.can_pin,
                "can_give_passports": admin.can_give_passports,
                "can_manage_money": admin.can_manage_money,
                "can_manage_partyies": admin.can_manage_partyies,
                "can_promote": admin.can_promote,
                "can_give_diplomas": admin.can_give_diplomas
            }
            if not hasattr(message, "chat"):
                result = frick[self.need_permission] and (message.message.chat.id == admin.chat or admin.chat == 0)
            else:
                result = frick[self.need_permission] and (message.chat.id == admin.chat or admin.chat == 0)
            return result
        return False
    
class CentraBankPersonal(BoundFilter):
    key = "central_bank_work"
    def __init__(self, *a, **k) -> None:
        pass

    async def check(self, message: Message) -> bool:
        personal = await DB.get_personal_cb()
        return message.from_user.id in personal

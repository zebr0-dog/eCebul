from typing import Optional

from .base_db import DB
from models import Admin

class AdminsDB(DB):
    async def set_admin(
        self,
        id: int,
        chat: int,
        can_mute: bool,
        can_ban: bool,
        can_pin: bool,
        can_manage_partyies: bool,
        can_manage_money: bool,
        can_give_passports: bool,
        can_promote: bool,
        **kwargs
    ) -> int:
        id, chat = int(id), int(chat)
        await self.connection.execute("""DELETE FROM ADMINS WHERE user_id=?""", (id,))
        await self.connection.execute("""
            INSERT INTO ADMINS VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (id, chat, can_mute, can_ban, can_pin, can_manage_money, can_manage_partyies, can_give_passports, can_promote))
        await self.commit()
        return 0

    async def get_admin(self, id: int) -> Optional[Admin]:
        async with self.connection.execute("""
            SELECT
                user_id, chat_id, can_mute, can_ban,
                can_pin, can_manage_money, can_manage_partyies,
                can_give_passports, can_promote
            FROM ADMINS WHERE user_id=?
        """, (id,)) as cursor:
            if (admin_db := await cursor.fetchone()):
                admin = Admin(*admin_db)
                return admin
            return None

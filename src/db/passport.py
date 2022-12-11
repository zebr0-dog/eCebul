import operator
from typing import Literal, Optional, Union

from .base_db import DB
from models import Passport
from variables import OPERATORS

class PassportDB(DB):
    async def save_passport(self, data: dict):
        """Save profile of user into db"""
        await self.connection.execute("""
            INSERT INTO PASSPORTS (
                user_id, name, surname, sex,
                username, birthdate, balance, status,
                job
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, tuple(data.values()))
        await self.commit()
        return 0
  
    async def get_passport(
        self,
        id: int=0,
        username: str="",
    ) -> Optional[Passport]:
        """Get user profile and return one as tuple"""
        async with self.connection.execute("""
            SELECT
                user_id, name, surname, sex, username,
                balance, status, job, emoji,
                partner, is_citizen, passport_photo,
                birthdate
            FROM PASSPORTS WHERE user_id=? OR username=?""", (id, username,)) as cursor:
            if (passport := (await cursor.fetchone())):
                passport_as_class = Passport(*passport)
                return passport_as_class
            else:
                return None
    
    async def update_passport(self, column: str, id: int, data: Union[str, int]):
        queryies ={
            "name": "UPDATE PASSPORTS SET name=(?) WHERE user_id=(?)",
            "surname": "UPDATE PASSPORTS SET surname=(?) WHERE user_id=(?)",
            "sex": "UPDATE PASSPORTS SET sex=(?) WHERE user_id=(?)",
            "job": "UPDATE PASSPORTS SET job=(?) WHERE user_id=(?)",
            "username": "UPDATE PASSPORTS SET username=(?) WHERE user_id=(?)",
            "balance": "UPDATE PASSPORTS SET balance=(?) WHERE user_id=(?)",
            "status": "UPDATE PASSPORTS SET status=(?) WHERE user_id=(?)",
            "emoji": "UPDATE PASSPORTS SET emoji=(?) WHERE user_id=(?)",
            "citizenship": "UPDATE PASSPORTS SET is_citizen=? WHERE user_id=?",
            "birthdate": "UPDATE PASSPORTS SET birthdate=? WHERE user_id=?"
        }
        query = queryies.get(column, "")
        data_for_query = (data, id)
        if query:
            await self.connection.execute(query, data_for_query)
            await self.commit()
            return 0
        return 1
    
    async def delete_passport(self, id: int) -> int:
        await self.connection.execute("DELETE FROM PASSPORTS WHERE user_id=(?)", (id,))
        return 0
    
    async def add_or_take_money(self, id: int, sum: int, operation: Literal["+", "-"]) -> int:
        if sum <= 0:
            return 1
        passport = await self.get_passport(id=id)
        if passport:
            new_balance = OPERATORS[operation](passport.balance, sum)
            if new_balance >= 0:
                await self.connection.execute("""
                    UPDATE PASSPORTS SET balance=? WHERE user_id=?
                """, (new_balance, id))
                await self.commit()
                return 0
            else:
                return 2
        else:
            return 3
    
    async def marry(self, id1: int, id2: int):
        profile1 = await self.get_passport(id1)
        profile2 = await self.get_passport(id2)
        if profile1 and profile2:
            if profile1.sex != profile2.sex:
                if (profile1.partner == 0) and (profile2.partner == 0):
                    await self.connection.executemany("""
                        UPDATE PASSPORTS SET partner=(?) WHERE user_id=(?)
                    """, 
                    (
                        (id2, id1),
                        (id1, id2)
                    )
                    )
                    return 0
                else:
                    return 1
            else:
                return 2
        else:
            return 3

    async def divorce(self, id1: int, id2: int):
        profile1 = await self.get_passport(id1)
        profile2 = await self.get_passport(id2)
        if profile1 and profile2:
            if profile1.partner == id2 and profile2.partner == id1:
                await self.connection.executemany("UPDATE CIJA SET partner=0 WHERE user_id=(?)", ((id1,), (id2,),))
                return 0
            else:
                return 1
        else:
            return 2

import operator
from typing import Literal, Optional, Union

from .base_db import DB
from models import Diploma
from variables import OPERATORS

class DiplomaDB(DB):
    async def save_diploma(self, data: dict):
        """Save profile of user into db"""
        await self.connection.execute("""
            INSERT INTO DIPLOMAS (
                user_id, name, surname, qualification,
                rector, date
            ) VALUES (?, ?, ?, ?, ?, ?)
        """, tuple(data.values()))
        await self.commit()
        return 0
  
    async def get_diploma(
        self,
        id: int=0,
        username: str="",
    ) -> Optional[Diploma]:
        """Get user profile and return one as tuple"""
        async with self.connection.execute("""
            SELECT
                user_id, name, surname, qualification,
                rector, date
            FROM DIPLOMAS WHERE user_id=?""", (id, username,)) as cursor:
            if (diploma := (await cursor.fetchone())):
                diploma_class = Diploma(*diploma)
                return diploma_class
            else:
                return None
    
    async def update_diploma(self, column: str, id: int, data: Union[str, int]):
        queryies ={
            "name": "UPDATE DIPLOMAS SET name=(?) WHERE user_id=(?)",
            "surname": "UPDATE DIPLOMAS SET surname=(?) WHERE user_id=(?)",
            "qualification": "UPDATE DIPLOMAS SET qualification=? WHERE user_id=?",
            "rector": "UPDATE DIPLOMAS SET rector=? WHERE user_id=?",
            "date": "UPDATE DIPLOMAS SET date=? WHERE user_id=?"
        }
        data_for_query = (data, id)
        if query:
            await self.connection.execute(query, data_for_query)
            await self.commit()
            return 0
        return 1

    async def delete_diploma(self, id: int) -> int:
        await self.connection.execute("DELETE FROM DIPLOMAS WHERE user_id=(?)", (id,))
        return 0

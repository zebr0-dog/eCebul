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
                user_id, student_name, student_surname, academy_name,
                date_course_start, date_course_end, average_grade
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """, tuple(data.values()))
        await self.commit()
        return 0
  
    async def get_diploma(
        self,
        user_id: int=0,
    ) -> Optional[Diploma]:
        """Get user profile and return one as tuple"""
        async with self.connection.execute("""
            SELECT
                user_id, student_name, student_surname, academy_name,
                date_course_start, date_course_end, average_grade
            FROM DIPLOMAS WHERE user_id=?""", (user_id,)) as cursor:
            if (diploma := (await cursor.fetchone())):
                diploma_class = Diploma(*diploma)
                return diploma_class
            else:
                return None
    
    async def update_diploma(self, column: str, id: int, data: Union[str, int]):
        queryies ={
            "student_name": "UPDATE DIPLOMAS SET name=(?) WHERE user_id=(?)",
            "student_surname": "UPDATE DIPLOMAS SET surname=(?) WHERE user_id=(?)",
            "academy_name": "UPDATE DIPLOMAS SET academy_name=? WHERE user_id=?",
            "date_course_start": "UPDATE DIPLOMAS SET date_course_start=? WHERE user_id=?",
            "date_course_end": "UPDATE DIPLOMAS SET date_course_end=? WHERE user_id=?",
            "average_grade": "UPDATE DIPLOMAS SET average_grade=? WHERE user_id=?"
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

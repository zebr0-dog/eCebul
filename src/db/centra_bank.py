from typing import Literal, List

from .base_db import DB
from .passport import PassportDB
from variables import OPERATORS

class CentraBankDB(PassportDB, DB):
    async def get_balance(self) -> int:
        query = await self.connection.execute("""
            SELECT balance FROM CENTRABANK
        """)
        result = await query.fetchone()
        if result:
            return result[0]
        return 0

    async def emission(self, amount: int, operation: Literal["+", "-"]) -> Literal[0, 1]:
        if amount > 0:
            balance = await self.get_balance()
            new_balance = OPERATORS[operation](balance, amount)
            await self.connection.execute("""
                UPDATE CENTRABANK SET balance=?
            """, (new_balance,))
            await self.commit()
            return 0
        return 1
    
    async def give_from_cb(self, amount: int, id: int) -> bool:
        if (await self.check_transaction(amount=amount, operation="+")):
            if not (await self.add_or_take_money(id, amount, "+")):
                await self.update_used()
                return True
        return False
    
    async def get_used(self):
        query = await self.connection.execute("""
            SELECT used FROM CENTRABANK
        """)
        result = await query.fetchone()
        if result:
            return result[0]
        return 0
    
    async def update_used(self):
        cash_money = await self.connection.execute_fetchall("""
            SELECT balance FROM PASSPORTS
        """)
        fund_money = await self.connection.execute_fetchall("""
            SELECT fund_balance FROM FUNDS
        """)
        used = 0
        for balance in cash_money:
            used += int(balance[0])
        for balance in fund_money:
            used += int(balance[0])
        await self.connection.execute("""
            UPDATE CENTRABANK SET used=?
        """, (used,))
        await self.commit()
        return
    
    async def get_personal_cb(self) -> List[int]:
        personal = await self.connection.execute_fetchall("""
            SELECT employee_id FROM CENTRABANK_PERSONAL
        """)
        list_of_personal = []
        for id in personal:
            list_of_personal.append(id[0])
        head = await self.get_head()
        list_of_personal.append(head)
        return list_of_personal
    
    async def add_personal(self, id: int):
        await self.connection.execute("""
            INSERT INTO CENTRABANK_PERSONAL VALUES (?)
        """, (id,))
        await self.update_passport("job", id, 18)
        await self.commit()
        return
    
    async def delete_personal(self, id: int):
        await self.connection.execute("""
            DELETE FROM CENTRABANK_PERSONAL WHERE employee_id=?
        """, (id,))
        await self.update_passport("job", id, 0)
        await self.commit()
        return
    
    async def change_head(self, id: int):
        old_head = await self.get_head()
        await self.connection.execute("""
            UPDATE CENTRABANK SET head=?
        """, (id,))
        await self.update_passport("job", old_head, 0)
        await self.update_passport("job", id, 12)
        await self.commit()
        return
    
    async def get_head(self) -> int:
        query = await self.connection.execute("""
            SELECT head FROM CENTRABANK
        """)
        res = await query.fetchone()
        if res:
            return res[0]
        return 0
    
    async def check_transaction(self, amount: int, operation: Literal["+", "-"]) -> bool:
        await self.update_used()
        used = await self.get_used()
        balance = await self.get_balance()
        return OPERATORS[operation](used, amount) <= balance

from typing import Dict, List, Optional, Union
from dataclasses import asdict

from .base_db import DB
from .passport import PassportDB
from models import Fund, Personal

class FundDB(PassportDB, DB):
    async def create_fund(self, owner_id: int, balance: int, name: str) -> int:
        await self.connection.execute("""
            INSERT INTO FUNDS (fund_owner_id, fund_balance, fund_name) VALUES (?, ?, ?)
        """, (owner_id, balance, name))
        await self.commit()
        return 0

    async def delete_fund(self, fund_id: int) -> int:
        id: int = int(fund_id)
        await self.connection.execute("""
            DELETE FROM FUNDS WHERE fund_id=?
        """, (id,))
        await self.commit()
        return 0

    async def get_all_funds(self) -> Optional[List[Fund]]:
        async with self.connection.execute("""
            SELECT fund_id, fund_owner_id, fund_balance, fund_name FROM FUNDS
        """) as cursor:
            funds = []
            if (res := (await cursor.fetchall())):
                for row in res:
                    funds.append(Fund(*row))
                return funds
        return None

    async def get_fund(self, fund_id: int) -> Optional[Fund]:
        fund_id = int(fund_id)
        async with self.connection.execute("""
            SELECT fund_id, fund_owner_id, fund_balance, fund_name FROM FUNDS WHERE fund_id=?
        """, (fund_id, )) as cursor:
            if (res := (await cursor.fetchone())):
                return Fund(*res)
            else:
                return None

    async def add_user_to_fund(self, fund_id: int, user_id: int, can_withdraw: bool, can_add_personal: bool):
        await self.connection.execute("""
            DELETE FROM FUNDS_PERSONAL WHERE fund_id=? AND employee_id=?
        """, (fund_id, user_id))
        await self.connection.execute("""
            INSERT INTO FUNDS_PERSONAL VALUES (?, ?, ?, ?)
        """, (fund_id, user_id, can_withdraw, can_add_personal,))
        await self.commit()
        return True

    async def delete_user_from_fund(self, fund_id: int, user_id:int):
        await self.connection.execute("""
            DELETE FROM FUNDS_PERSONAL WHERE employee_id=? AND fund_id=?
        """, (user_id, fund_id,))
        await self.commit()
        return 0
    
    async def get_personal(self, fund_id: int) -> Optional[Dict[int, Personal]]:
        async with self.connection.execute("""
            SELECT employee_id, can_withdraw, can_add_personal FROM FUNDS_PERSONAL WHERE fund_id=?
        """, (fund_id,)) as cursor:
            if (res := (await cursor.fetchall())):
                personal = {}
                for person in res:
                    employee = Personal(*person)
                    personal[employee.id] = employee
                return personal
            else:
                return None
    
    async def check_permission(self, user_id: int, fund_id: int, permission: str) -> bool:
        """ Check if user has a permission to do smth in the fund.
        :param parmission accept "withdraw" or "add_personal"
        """
        queries = {
            "withdraw": "SELECT can_withdraw FROM FUNDS_PERSONAL WHERE fund_id=? AND employee_id=?",
            "add_personal": "SELECT can_add_personal FROM FUNDS_PERSONAL WHERE fund_id=? AND employee_id=?",
        }
        async with self.connection.execute(queries.get(permission), (fund_id, user_id,)) as cursor:
            if (res := (await cursor.fetchone())):
                return bool(res)
        return False

    async def withdraw_money(self, user_id: int, fund_id: int, amount: int):
        if amount > 0:
            fund = await self.get_fund(fund_id=fund_id)
            if fund:
                has_permission = await self.check_permission(user_id=user_id, fund_id=fund_id, permission="withdraw")
                if has_permission or user_id == fund.owner:
                    new_balance = fund.balance - amount
                    if new_balance >= 0:
                        await self.connection.execute("""
                            UPDATE FUNDS SET fund_balance=? WHERE fund_id=?
                        """, (new_balance, fund_id))
                        await self.add_or_take_money(user_id, amount, "+")
                        await self.commit()
                        return 0, fund.name
                    else:
                        return 1
                else:
                    return 2
            else:
                return 3
        else:
            return 4

    async def replenish_money(self, fund_id: int, user_id: int, amount: int):
        if amount > 0:
            fund = await self.get_fund(fund_id=fund_id)
            if fund:
                take_money = await self.add_or_take_money(id=user_id, sum=amount, operation="-")
                if take_money == 0:
                    new_banalce = fund.balance + amount
                    await self.connection.execute("""
                        UPDATE FUNDS SET fund_balance=? WHERE fund_id=?
                    """, (new_banalce, fund_id))
                    await self.commit()
                    return 0, fund.name
                else:
                    return 1
            else:
                return 2
        else:
            return 3
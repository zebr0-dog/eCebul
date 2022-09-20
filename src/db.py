from ctypes import Union
from optparse import Option
from typing import Optional, Tuple
import aiosqlite
import operator
from functools import wraps

def connection(fn):
    @wraps(fn)
    async def wrapper(*args, **kwargs):
        connect = await aiosqlite.connect('cija.db')
        res = await fn(*args, **kwargs, connect=connect)
        await connect.commit()
        await connect.close()
        return res
    return wrapper

@connection
async def create_table(*arg, connect: aiosqlite.Connection):
    """ Create all needed tables for correct work of bot """
    await connect.execute("""
        CREATE TABLE IF NOT EXISTS CIJA (
            user_id int,
            name text,
            surname text,
            sex text,
            username text,
            balance int,
            info text,
            job text,
            active bool
        )
    """)
    await connect.execute("""
        CREATE TABLE IF NOT EXISTS ADMINS (
            user_id int,
            rang int,
            chat_id int
        )
    """)
    await connect.execute("""
        CREATE TABLE IF NOT EXISTS PARTYIES (
            party_id INT FOREIGN_KEY AUTOINCREMENT,
            name TEXT,
            owner INT
        )
    """)
    return 0

@connection
async def save_passport(data: dict, connect):
    """Save profile of user into db"""
    await connect.execute("""
        INSERT INTO CIJA VALUES (?, ?, ?, ?, ?, ?, ?, ?, 1)
    """, tuple(data.values()))
    return 0

@connection
async def get_passport(id: int, connect: aiosqlite.Connection) -> tuple:
    """Get user profile and return one as tuple"""
    async with connect.execute("""
        SELECT (
            name, surname, sex, username,
            job, balance, info, active 
        ) FROM CIJA WHERE user_id=?
    """, (id,)) as cursor:
        if (passport := (await cursor.fetchone())):
            name, surname, sex, username, job, balance, info, active = passport
            return name, surname, sex, username, job, balance, info, active
        else:
            return None

@connection
async def check_is_user_exist(id: int, connect: aiosqlite.Connection) -> bool:
    """Return True if user have paasport and False if not"""
    async with connect.execute("""
        SELECT user_id FROM CIJA WHERE user_id=(?)
    """, (id,)) as cursor:
        return bool(cursor)

@connection
async def update_data(column: str, id: int, data: str, connect: aiosqlite.Connection):
    """Update data in passport"""
    queryies ={
        "name": "UPDATE CIJA SET name=(?) WHERE user_id=(?)",
        "surname": "UPDATE CIJA SET surname=(?) WHERE user_id=(?)",
        "sex": "UPDATE CIJA SET sex=(?) WHERE user_id=(?)",
        "job": "UPDATE CIJA SET job=(?) WHERE user_id=(?)",
        "username": "UPDATE CIJA SET username=(?) WHERE user_id=(?)",
        "balance": "UPDATE CIJA SET balance=(?) WHERE user_id=(?)",
        "info": "UPDATE CIJA SET info=(?) WHERE user_id=(?)",
        "activity": "UPDATE CIJA SET active=(?) WHERE user_id=(?)",
    }
    query = queryies.get(column, "")
    data = (data, id)
    if query:
        await connect.execute(query, (*data,))
        return 0
    return 1

@connection
async def delete_passport(id: int, connect: aiosqlite.Connection) -> int:
    await connect.execute("DELETE FROM CIJA WHERE user_id=(?)", (id,))
    return 0

@connection
async def set_admin(id: int, rang: int, chat: int, connect: aiosqlite.Connection) -> int:
    await connect.execute("""
        INSERT OR REPLACE INTO ADMINS VALUES (?, ?, ?)
    """, (id, rang, chat,))
    return 0

@connection
async def get_admin(id: int, connect: aiosqlite.Connection) -> int:
    async with connect.execute("""
        SELECT rang, chat FROM ADMINS WHERE user_id=?
    """, (id,)) as cursor:
        if (res := (await cursor.fetchall())):
            new_res = {}
            for i in res:
                rang, chat = i
                new_res[chat] = rang
            return new_res
        else:
            return 0

@connection
async def add_or_take_money(id, sum, operation, connect):
    sum = int(sum)
    if sum < 0:
        return 1
    operators = {
        "+": operator.add,
        "-": operator.sub,
    }
    async with connect.execute("""
        SELECT balance FROM CIJA where user_id=?
    """, (id,)) as cursor:
        if (result := (await cursor.fetchone())):
            balance = result[0]
            new_balance = operators[operation](balance, sum)
            await connect.execute("""
                UPDATE CIJA SET balance=? WHERE user_id=?
            """, (new_balance, id))
            return 0
        else:
            return 2

@connection
async def get_all_partyies(connect):
    async with connect.execute("""
        SELECT name, owner FROM PARTYIES
    """) as cursor:
        res = await cursor.fetchall()
        if res:
            new_res = {}
            for name, owner in res:
                new_res[name] = owner
            return new_res
        else:
            return {}

@connection
async def get_party(owner: int, connect):
    await connect.execute("""
        SELECT name, party_id FROM PARTYIES
    """)
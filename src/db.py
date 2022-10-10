from hashlib import new
from typing import Dict, Union
from xmlrpc.client import Boolean
import aiosqlite
import operator
from functools import wraps
from json import dumps, loads
from pickletools import read_bytes1
from sqlite3 import connect
from types import new_class

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
            emoji text DEFAULT '👤'
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
            party_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            owner INT
        )
    """)
    await connect.execute("""
        CREATE TABLE IF NOT EXISTS PARTYIES_MEMBERS (
            party_id int,
            member_id int
        )
    """)
    await connect.execute("""
        CREATE TABLE IF NOT EXISTS CANDIDATS (
            id int,
            program text,
            votes int
        )
    """)
    await connect.execute("""
        CREATE TABLE IF NOT EXISTS VOTED (
            id int,
            vote_for int
        )
    """)
    await connect.execute("""
        CREATE TABLE IF NOT EXISTS STATUS_OF_VOTE (
            status int
        )
    """)
    #creating fund table
    await connect.execute("""
        CREATE TABLE IF NOT EXISTS FUNDS (
            fund_id int,
            fund_owner_id int,
            fund_balance int,
            fund_name text,
            fund_personal text
        )
     """)
    await connect.execute("""
        CREATE TABLE IF NOT EXISTS SHOP (
            shop_id INTEGER PRIMARY KEY NOT NULL,
            shop_title text NOT NULL,
            shop_owner_id int NOT NULL,
            default_message text
        )
     """)
    await connect.execute("""
        CREATE TABLE IF NOT EXISTS ITEM (
            item_id INTEGER PRIMARY KEY NOT NULL,
            item_count int NOT NULL,
            item_name text NOT NULL,
            description text NOT NULL,
            shop_id int NOT NULL,
            cost int,
            status text
        )
     """)
    await connect.execute("""
        CREATE TABLE IF NOT EXISTS BOUGHT_ITEM (
            owner_item_id int NOT NULL,
            item_id INTEGER NOT NULL,
            item_name text NOT NULL,
            description text NOT NULL,
            status text
        )
     """)
    return 0

@connection
async def save_passport(data: dict, connect):
    """Save profile of user into db"""
    await connect.execute("""
        INSERT INTO CIJA (
            user_id, name, surname, sex,
            username, balance, info, job
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, tuple(data.values()))
    return 0

@connection
async def get_passport_from_username(username: str, connect: aiosqlite.Connection) -> tuple:
    """Get user profile and return one as tuple"""
    async with connect.execute("""
        SELECT
            name, surname, sex, user_id,
            job, balance, info, emoji
        FROM CIJA WHERE username=?
     """, (username,)) as cursor:
        if (passport := (await cursor.fetchone())):
            name, surname, sex, user_id, job, balance, info, emoji = passport
            return name, surname, user_id, sex, job, balance, info, emoji
        else:
            return None

@connection
async def get_passport(id: int, connect: aiosqlite.Connection) -> tuple:
    """Get user profile and return one as tuple"""
    async with connect.execute("""
        SELECT
            name, surname, sex, username,
            job, balance, info, emoji
        FROM CIJA WHERE user_id=?
    """, (id,)) as cursor:
        if (passport := (await cursor.fetchone())):
            name, surname, sex, username, job, balance, info, emoji = passport
            return name, surname, sex, username, job, balance, info, emoji
        else:
            return None

@connection
async def get_name(connect, id: int):
    async with connect.execute("""
        SELECT
            name, surname, username
        FROM CIJA WHERE user_id=?
    """, (id,)) as cursor:
        if (res := (await cursor.fetchone())):
            name, surname, username = res
        return name, surname, username

@connection
async def check_is_user_exist(id: int, connect: aiosqlite.Connection) -> bool:
    """Return True if user have paasport and False if not"""
    async with connect.execute("""
        SELECT user_id FROM CIJA WHERE user_id=?
    """, (id,)) as cursor:
        exist = await cursor.fetchone()
        return bool(exist)

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
        "emoji": "UPDATE CIJA SET emoji=(?) WHERE user_id=(?)"
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
    id, rang, chat = int(id), int(rang), int(chat)
    await connect.execute("""
        INSERT OR REPLACE INTO ADMINS VALUES (?, ?, ?)
    """, (id, rang, chat,))
    return 0

@connection
async def get_admin(id: int, connect: aiosqlite.Connection) -> int:
    async with connect.execute("""
        SELECT rang, chat_id FROM ADMINS WHERE user_id=?
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
    if sum <= 0:
        return 1
    exist = await check_is_user_exist(id)
    if exist:
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
                if new_balance >= 0:
                    await connect.execute("""
                        UPDATE CIJA SET balance=? WHERE user_id=?
                    """, (new_balance, id))

                    return 0
                else:
                    return 3
            else:
                return 2
    else:
        return 4

@connection
async def get_all_partyies(connect):
    async with connect.execute("""
        SELECT party_id, name, owner FROM PARTYIES
    """) as cursor:
        if (res := (await cursor.fetchall())):
            new_res = {}
            for row in res:
                async with connect.execute("""
                    SELECT member_id FROM PARTYIES_MEMBERS WHERE party_id=?
                """, (row[0],)) as cursor2:
                    _count = len(list((await cursor2.fetchall())))
                    _owner = await get_passport(row[2])
                    owner_name, owner_username = _owner[0], _owner[3]
                    new_res[row[1]] = {
                        "owner": {
                            "name": owner_name,
                            "username": owner_username
                        },
                        "members_count": _count
                    }
            return new_res
        else:
            return {}

@connection
async def get_party(id: int, connect):
    party_id = await connect.execute("""
        SELECT party_id FROM PARTYIES_MEMBERS WHERE member_id=?
    """, (id,))
    party_id = await party_id.fetchone()
    if party_id:
        party_id = party_id[0]
        party_db = await connect.execute("""
            SELECT owner, name, party_id FROM PARTYIES WHERE party_id=?
        """, (party_id,))
        if (party := (await party_db.fetchone())):
            owner, party_name, party_id = party
            members = await connect.execute("""
                SELECT member_id FROM PARTYIES_MEMBERS where party_id=?
            """, (party_id,))
            members = await members.fetchall()
            new_members = []
            for member in members:
                member = member[0]
                passport = await get_passport(member)
                if passport:
                    name, *bloat = passport
                    new_members.append(name)
                else:
                    continue
            party = {
                "name": party_name,
                "members": new_members,
                "owner": (owner==id),
            }
            return party
    return 0

@connection
async def add_member_to_party(member_id: int, owner_id: int, connect):
    res = await connect.execute("""
        SELECT party_id FROM PARTYIES WHERE owner=?
    """, (owner_id,))
    if (party_id := (await res.fetchone())):
        party_id = party_id[0]
        await connect.execute("""
            INSERT OR REPLACE INTO PARTYIES_MEMBERS VALUES (?, ?)
        """, (party_id, member_id,))
        return 0
    else:
        return 1

@connection
async def delete_member_from_party(member_id, connect):
    await connect.execute("""
        DELETE FROM PARTYIES_MEMBERS WHERE member_id=?
    """, (member_id,))
    return 0

@connection
async def save_party(owner, name, first, second, connect):
    owner, first, second = int(owner), int(first), int(second)
    await connect.execute("""
        INSERT OR REPLACE INTO PARTYIES (name, owner) VALUES (?, ?)
    """, (name, owner))
    party_id = await connect.execute("""
        SELECT party_id FROM PARTYIES WHERE owner=?
    """, (owner,))
    party_id = await party_id.fetchone()
    party_id = party_id[0]
    await connect.executemany("""
        INSERT OR REPLACE INTO PARTYIES_MEMBERS (party_id, member_id) VALUES (?, ?)
    """, (
            [
                (
                    party_id,
                    first
                ),
                (
                    party_id,
                    second
                ),
                (
                    party_id,
                    owner
                )
            ]
        )
    )

@connection
async def get_count_of_candidats(connect):
    async with connect.execute("""
        SELECT id FROM CANDIDATS
    """) as cursor:
        res = await cursor.fetchall()
        if res:
            return len(res)
        return 0

@connection
async def save_candidate(id, program, connect):
    status = await connect.execute("""
        SELECT status FROM STATUS_OF_VOTE
    """)
    status = (await status.fetchone())[0]
    if status == 2:
        count_of_candidats = await get_count_of_candidats()
        if count_of_candidats < 12:
            info = (await get_passport(id))[6]
            if info in [
                "🎗️ Середняк, розуміє головні Державні аспекти!",
                "🎖️ Ветеран, знається на Державі"
            ]:
                votes = await connect.execute("""
                    SELECT votes FROM CANDIDATS WHERE id=?
                """, (id,))
                votes = await votes.fetchone()
                if votes:
                    votes = votes[0]
                else:
                    votes = 0
                await connect.execute("""
                    INSERT OR REPLACE INTO CANDIDATS VALUES (?, ?, ?)
                """, (id, program, votes))
                return 0
            else:
                return 2
        else:
            return 3
    else:
        return 1

@connection
async def get_all_candidats(connect):
    status = await connect.execute("""
        SELECT status FROM STATUS_OF_VOTE
    """)
    status = (await status.fetchone())[0]
    if status == 3:
        async with connect.execute("""
                SELECT id, votes FROM CANDIDATS
            """) as cursor:
            candidates = {}
            candidates_from_db = await cursor.fetchall()
            for row in candidates_from_db:
                id, votes = row
                name, surname, sex, username, *bloat = await get_passport(id)
                candidates[id] = {
                    "id": id,
                    "name": name,
                    "surname": surname,
                    "votes": votes,
                    "username": username[1::]
                }
            return candidates
    else:
        return 1

@connection
async def get_all_candidates(connect):
    async with connect.execute("""
    SELECT id, votes FROM CANDIDATS
    """) as cursor:
        candidates = {}
        candidates_from_db = await cursor.fetchall()
        for row in candidates_from_db:
            id, votes = row
            name, surname, sex, username, *bloat = await get_passport(id)
            candidates[id] = {
                "id": id,
                "name": name,
                "surname": surname,
                "votes": votes,
                "username": username[1::]
            }
        return candidates

@connection
async def get_candidate(id: int, connect) -> Dict[str, Union[str, int]]:
    status = await connect.execute("""
        SELECT status FROM STATUS_OF_VOTE
    """)
    status = (await status.fetchone())[0]
    if status == 3:
        async with connect.execute("""
            SELECT id, program, votes FROM CANDIDATS WHERE id=?
        """, (id,)) as cursor:
            candidate_db = await cursor.fetchone()
            if candidate_db:
                id, program, votes = candidate_db
                name, surname, sex, username, *bloat = await get_passport(id)
                party = await get_party(id)
                if not party:
                    party = {}
                candidate = {
                    "id": id,
                    "name": name,
                    "surname": surname,
                    "username": username[1::],
                    "party": party.get("name"),
                    "program": program,
                    "votes": votes
                }
                return candidate
            else:
                return 0
    else:
        return 1

@connection
async def vote(id: int, voter_id: int, connect):
    status = await connect.execute("""
        SELECT status FROM STATUS_OF_VOTE
    """)
    status = (await status.fetchone())[0]
    if status == 3:
        info = (await get_passport(voter_id))[6]
        if info in [
            "🎗️ Середняк, розуміє головні Державні аспекти!",
            "🎖️ Ветеран, знається на Державі"
        ]:
            async with connect.execute("""
                SELECT id FROM VOTED WHERE id=?
            """, (voter_id,)) as cursor2:
                was_voted = await cursor2.fetchone()
                if not was_voted:
                    candidate = await get_candidate(id)
                    if type(candidate) == dict and "votes" in candidate:
                        votes = candidate["votes"]
                        votes += 1
                        await connect.execute("""
                            DELETE FROM CANDIDATS WHERE id=?
                        """, (id,))
                        await connect.execute("""
                            INSERT INTO CANDIDATS VALUES (?, ?, ?)
                        """, (id, candidate["program"], votes))
                        await connect.execute("""
                            INSERT INTO VOTED VALUES (?, ?)
                        """, (voter_id, id))
                        return 0
                    else:
                        return 1
                else:
                    return 2
        else:
            return 4
    else:
        return 3

@connection
async def change_status_of_vote(status, connect):
    # 1 - voting is'nt running
    # 2 - register of candidats is running
    # 3 - voting is running
    await connect.execute("""
        DELETE FROM STATUS_OF_VOTE
    """)
    await connect.execute("""
        INSERT INTO STATUS_OF_VOTE VALUES (?)
    """, (status,))
    if status == 1:
        candidats = await get_all_candidats()
        if not candidats:
            candidats = {}
        await connect.execute("""
            DELETE FROM VOTED
        """)
        await connect.execute("""
            DELETE FROM CANDIDATS
        """)
        return candidats
    return 0

@connection
async def create_fund(owner_id: int, balance: int, name:str, connect):
    async with connect.execute("""
        SELECT fund_id, fund_owner_id, fund_balance, fund_name, fund_personal FROM FUNDS
    """) as cursor:
        if (res := (await cursor.fetchall())):
            res = res
    """Create fund"""
    await connect.execute("""
        INSERT INTO FUNDS VALUES (?, ?, ?, ?, ?)
    """, (int(len(res)+1), owner_id, balance, name, f"[{owner_id}]"))
    return 0

@connection
async def delete_fund(fund_id: int, connect):
    fund_id = int(fund_id)
    """Delete fund"""
    await connect.execute("""
        DELETE FROM FUNDS WHERE fund_id=?
    """, (fund_id,))
    return 0

@connection
async def get_all_funds(connect):
    async with connect.execute("""
        SELECT fund_id, fund_owner_id, fund_balance, fund_name, fund_personal FROM FUNDS
    """) as cursor:
        if (res := (await cursor.fetchall())):
            return res

@connection
async def get_fund_by_id(fund_id: int, connect):
    fund_id = int(fund_id)
    async with connect.execute("""
        SELECT fund_id, fund_owner_id, fund_balance, fund_name, fund_personal FROM FUNDS WHERE fund_id=?
    """, (fund_id, )) as cursor:
        if (res := (await cursor.fetchall())):
            return res

@connection
async def add_user_to_fund(fund_id: int, user_id:int, connect):
    async with connect.execute("""
        SELECT fund_id, fund_owner_id, fund_balance, fund_name, fund_personal FROM FUNDS WHERE fund_id=?
    """, (fund_id, )) as cursor:
        if (res := (await cursor.fetchall())):
            for line in res:
                res = line[4]
    res = loads(res)
    if int(user_id) not in res:
        res.append(int(user_id))
    await connect.execute("""
            UPDATE FUNDS SET fund_personal=? WHERE fund_id=?
        """, (dumps(res), fund_id))
        
    return True

@connection
async def delete_user_from_fund(fund_id: int, user_id:int, connect):
    async with connect.execute("""
        SELECT fund_id, fund_owner_id, fund_balance, fund_name, fund_personal FROM FUNDS WHERE fund_id=?
    """, (fund_id, )) as cursor:
        if (res := (await cursor.fetchall())):
            for line in res:
                res = line[4]
    res = loads(res)
    if int(res[0]) != int(user_id):
        res.pop(res.index(int(user_id)))
        await connect.execute("""
                UPDATE FUNDS SET fund_personal=? WHERE fund_id=?
            """, (dumps(res), fund_id))
            
        return True
    else:
        return False
    
@connection
async def check_user_ownership(user_id: int, connect):
    async with connect.execute("""
        SELECT fund_personal FROM FUNDS
    """) as cursor:
        if (res := (await cursor.fetchall())):
            return res

@connection
async def withdraw_fund_money(fund_id: int, amount: id, connect):
    if '-' not in str(amount):
        async with connect.execute(
            """
            SELECT fund_balance, fund_name FROM FUNDS WHERE fund_id=?
            """, (fund_id,)) as cursor:
            if (res := (await cursor.fetchall())):
                fund_balance = int(res[0][0])
                fund_name = str(res[0][1])
        
        amount = int(amount)
        
        if fund_id == 1:
            fund_balance -= amount
            await connect.execute("""
                            UPDATE FUNDS SET fund_balance=? WHERE fund_id=?
                        """, (fund_balance, 1)) 
            return (0, fund_name)
        else:
            fund_balance -= amount
            async with connect.execute(
            """
            SELECT fund_balance FROM FUNDS WHERE fund_id=?
            """, (1,)) as cursor:
                if (res := (await cursor.fetchall())):
                    main_fund_balance = int(res[0][0])
                    main_fund_balance += amount
                    await connect.execute("""
                            UPDATE FUNDS SET fund_balance=? WHERE fund_id=?
                        """, (main_fund_balance, 1))
                    
            await connect.execute("""
                            UPDATE FUNDS SET fund_balance=? WHERE fund_id=?
                        """, (fund_balance, fund_id))     
            
            return (0, fund_name)
        
@connection
async def replenish_fund_money(fund_id: int, amount: int, user_id: int, transaction: bool, connect):
    if '-' not in str(amount):
        if int(amount) <= 0:
            return
        async with connect.execute(
            """
            SELECT fund_balance, fund_name FROM FUNDS WHERE fund_id=?
            """, (fund_id,)) as cursor:
            if (res := (await cursor.fetchall())):
                fund_balance = int(res[0][0])
                fund_name = str(res[0][1])
        amount = int(amount)
        if not transaction:
            fund_balance += amount
            await connect.execute("""
                            UPDATE FUNDS SET fund_balance=? WHERE fund_id=?
                        """, (fund_balance, 1)) 
            return (0, fund_name)
        else:
            fund_balance += amount
            async with connect.execute(
                """
                SELECT balance FROM CIJA WHERE user_id=?
                """, (user_id,)) as cursor:
                if (res := (await cursor.fetchall())):
                    new_user_balance = int(res[0][0])
                    if new_user_balance < amount:
                        return
                    new_user_balance -= amount
                    await connect.execute("""
                            UPDATE CIJA SET balance=? WHERE user_id=?
                        """, (new_user_balance, user_id))
            await connect.execute("""
                            UPDATE FUNDS SET fund_balance=? WHERE fund_id=?
                        """, (fund_balance, fund_id))     
            return (0, fund_name)
    
@connection
async def take_fund_money(fund_id: int, amount: id, user_id: int,  connect):
    if '-' not in str(amount):
        async with connect.execute(
            """
            SELECT fund_balance, fund_name FROM FUNDS WHERE fund_id=?
            """, (fund_id,)) as cursor:
            if (res := (await cursor.fetchall())):
                fund_balance = int(res[0][0])
                fund_name = str(res[0][1])
        amount = int(amount)
        if fund_balance >= amount:
            fund_balance -= amount
            async with connect.execute(
                """
                SELECT balance FROM CIJA WHERE user_id=?
                """, (user_id,)) as cursor:
                if (res := (await cursor.fetchall())):
                    new_user_balance = int(res[0][0])
                    
                    new_user_balance += amount
                    
                    await connect.execute("""
                                    UPDATE CIJA SET balance=? WHERE user_id=?
                        """, (new_user_balance, user_id))
                    
                    await connect.execute("""
                                    UPDATE FUNDS SET fund_balance=? WHERE fund_id=?
                                """, (fund_balance, fund_id))     
            
            return (0, fund_name)
        
@connection
async def list_shop(connect):
    async with connect.execute("""
        SELECT shop_title FROM SHOP ORDER BY shop_id DESC
    """) as cursor:
        if (res := (await cursor.fetchall())):
            return res
            
@connection
async def my_shop(connect, owner_id: int):
    async with connect.execute("""
        SELECT shop_title FROM SHOP WHERE shop_owner_id = ? ORDER BY shop_id DESC
    """, (owner_id,)) as cursor:
        if (res := (await cursor.fetchall())):
            return res
            
@connection
async def is_my_shop(connect, shop_id: int, sender_id: int):
    shop = await connect.execute("""
        SELECT shop_owner_id FROM SHOP WHERE shop_id = ?
    """, (shop_id,))
    shop = (await shop.fetchone())[0]
    if shop == sender_id:
        return True
    else:
        return False
            
@connection
async def list_item(connect, shopid: int):
    async with connect.execute("""
        SELECT item_name FROM ITEM WHERE shop_id = ? 
    """, (shopid,)) as cursor:
        if (res := (await cursor.fetchall())):
            return res
           
@connection
async def id_shop(connect, title: str):
    async with connect.execute("""
        SELECT shop_id FROM SHOP WHERE shop_title = ?
    """, (title,)) as cursor:
        if (res := (await cursor.fetchone())):
            return res

@connection
async def def_msg(connect, title: str):
    async with connect.execute("""
        SELECT default_message FROM SHOP WHERE shop_title = ?
    """, (title,)) as cursor:
        if (res := (await cursor.fetchone())):
            return res
@connection
async def title_shop(connect, id: int):
    async with connect.execute("""
        SELECT shop_title FROM SHOP WHERE shop_id = ? 
    """, (id,)) as cursor:
        if (res := (await cursor.fetchall())):
            return res

@connection
async def item(connect, id: int):
    async with connect.execute("""
        SELECT item_name, shop_id, cost, status, description FROM ITEM WHERE item_id = ? 
    """, (id,)) as cursor:
        if (res := (await cursor.fetchall())):
            return res

@connection
async def buy_item(connect, id_item:int, id_buyer:int, name:str, desc:str, status:str):
    owner_id, items_num = int(owner_id), int(items_num)
    await connect.execute("""
        INSERT INTO BOUGHT_ITEM (owner_item_id, item_id) VALUES (?, ?, ?, ?, ?)
    """, (id_buyer, id_item, name, desc, status))
    
async def bought(connect, id_b:int):
        async with connect.execute("""
        SELECT item_name, description, status FROM ITEM WHERE owner_item_id = ? ORDER BY item DESC
    """, (id,)) as cursor:
            if (res := (await cursor.fetchall())):
                return res

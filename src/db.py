from itertools import count
from re import S
from typing import Dict, Union
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
        SELECT
            name, surname, sex, username,
            job, balance, info, active
        FROM CIJA WHERE user_id=?
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
            return count(res)
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
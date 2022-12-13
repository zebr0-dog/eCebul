from typing import List, Optional

from .base_db import DB
from .passport import PassportDB
from models import Party, Member

class PartyDB(PassportDB, DB):
    async def get_all(self) -> Optional[List[Party]]:
        async with self.connection.execute("""
            SELECT * FROM PARTIES
        """) as cursor:
            parties = []
            if (res := (await cursor.fetchall())):
                for row in res:
                    parties.append(Party(*row))
                return parties
        return None

    async def get_party_by_user(self, user_id: int) -> Optional[Party]:
        party_result = await self.connection.execute("SELECT * FROM PARTIES WHERE party_id=(SELECT party_id FROM PARTIES_MEMBERS WHERE member_id=?)", (user_id,))
        party_db = await party_result.fetchone()
        if party_db:
            print(party_db[2])
            party = Party(*party_db)
            return party
        else:
            return None

    async def get_party_by_id(self, party_id: int) -> Optional[Party]:
            party_db = await self.connection.execute("""
                SELECT * FROM PARTIES WHERE party_id=?
            """, (party_id,))
            party_fetched = await party_db.fetchone()
            if party_fetched:
                return Party(*party_fetched)
            return None

    async def add_member(self, member_id: int, user_id: int) -> int:
        party = await self.get_party_by_user(user_id=user_id)
        if party:
            await self.delete_member(member_id=member_id)
            await self.connection.execute("""
                INSERT INTO PARTIES_MEMBERS VALUES (?, ?)
            """, (party.id, member_id,))
            await self.commit()
            return 0
        else:
            return 1

    async def delete_member(self, member_id: int) -> int:
        await self.connection.execute("""
            DELETE FROM PARTIES_MEMBERS WHERE member_id=?
        """, (member_id,))
        await self.commit()
        return 0

    async def save_party(self, owner: int, name: str, first: int, second: int) -> int:
        owner, first, second = int(owner), int(first), int(second)
        if len({owner, first, second}) == 3:
            new_party = await self.connection.execute("""
                INSERT OR REPLACE INTO PARTIES (name, owner) VALUES (?, ?)
            """, (name, owner))
            party_id = new_party.lastrowid
            await self.connection.executemany("""
                INSERT OR REPLACE INTO PARTIES_MEMBERS (party_id, member_id) VALUES (?, ?)
            """, ([
                        (party_id, first),
                        (party_id, second),
                        (party_id, owner)
                ]))
            await self.commit()
            return 0
        else:
            return 1
    
    async def delete_party(self, party_id: int) -> int:
        await self.connection.execute("DELETE FROM PARTIES WHERE party_id=?", (party_id,))
        await self.connection.execute("DELETE FROM PARTIES_MEMBERS WHERE party_id=?", (party_id,))
        await self.commit()
        return 0
    
    async def get_members(self, party_id: int) -> Optional[List[Member]]:
        party = await self.get_party_by_id(party_id=party_id)
        if party:
            res = await self.connection.execute("SELECT member_id, can_add_members FROM PARTIES_MEMBERS WHERE party_id=?", (party_id,))
            if (members := await res.fetchall()):
                members_list = []
                for member in members:
                    member_passport = await self.get_passport(id=member[0])
                    if member_passport:
                        member_as_class = Member(
                            id=member_passport.id,
                            name=member_passport.name,
                            surname=member_passport.surname,
                            can_add_members=member[1]
                        )
                        members_list.append(member_as_class)
                return members_list
        return None

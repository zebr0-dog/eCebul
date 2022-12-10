from typing import Dict, Optional, Union

from .base_db import DB
from .passport import PassportDB
from .party import PartyDB
from models import StatusOfVoting, Candidate

class VoteDB(PartyDB, PassportDB, DB):
    async def get_count_of_candidats(self) -> int:
        async with self.connection.execute("""
            SELECT COUNT (id) FROM CANDIDATES
        """) as cursor:
            res = await cursor.fetchone()
            if res:
                return res[0]
            return 0

    async def save_candidate(self, id: int, program: str) -> int:
        status = self.get_status_of_vote()
        if status == StatusOfVoting.REGISTER_OF_CANDIDATES:
            count_of_candidats = await self.get_count_of_candidats()
            if count_of_candidats < 12:
                candidat_passport = await self.get_passport(id)
                if candidat_passport:
                    if candidat_passport.status >= 2 and candidat_passport.is_citizen:
                        candidat = await self.get_candidate(id=id)
                        votes = ...
                        if type(candidat) == Candidate:
                            votes = candidat.votes  # type: ignore
                        else:
                            votes = 0
                        await self.connection.execute("""
                            INSERT OR REPLACE INTO CANDIDATES VALUES (?, ?, ?)
                        """, (id, program, votes))
                        await self.commit()
                        return 0
                    else:
                        return 1
                else:
                    return 2
            else:
                return 3
        else:
            return 4

    async def get_all_candidats(self) -> Union[Dict[int, Candidate], int]:
        status = await self.get_status_of_vote()
        if status == StatusOfVoting.VOTING:
            async with self.connection.execute("""
                    SELECT id, votes, program FROM CANDIDATES
                """) as cursor:
                candidates = {}
                candidates_from_db = await cursor.fetchall()
                for row in candidates_from_db:
                    id, votes, program = row
                    candidate_passport = await self.get_passport(id)
                    if candidate_passport:
                        candidates[id] = Candidate(
                            id=id,
                            name=candidate_passport.name,
                            surname=candidate_passport.surname,
                            votes=votes,
                            username=candidate_passport.username,
                            program=program,
                            party=""
                        )
                return candidates
        else:
            return 1

    async def get_candidate(self, id: int) -> Union[Candidate, int]:
        status = await self.get_status_of_vote()
        if status == StatusOfVoting.VOTING:
            async with self.connection.execute("""
                SELECT program, votes FROM CANDIDATES WHERE id=?
            """, (id,)) as cursor:
                candidate_db = await cursor.fetchone()
                if candidate_db:
                    program, votes = candidate_db
                    candidate_passport = await self.get_passport(id)
                    if candidate_passport:
                        party = await self.get_party_by_user(id)
                        if not party:
                            party_name = ""
                        else:
                            party_name = party.name
                        candidate = Candidate(
                            id=id,
                            name=candidate_passport.name,
                            surname=candidate_passport.surname,
                            username=candidate_passport.username,
                            party=party_name,
                            program=program,
                            votes=votes
                        )
                        return candidate
                    else:
                        return 1
                else:
                    return 2
        else:
            return 3

    async def vote(self, id: int, voter_id: int) -> int:
        status = await self.get_status_of_vote()
        if status == StatusOfVoting.VOTING:
            passport_of_voter = await self.get_passport(id=voter_id)
            if passport_of_voter:
                if passport_of_voter.status >= 2 and passport_of_voter.is_citizen:
                    async with self.connection.execute("""
                        SELECT id FROM VOTED WHERE id=?
                    """, (voter_id,)) as cursor:
                        was_voted = await cursor.fetchone()
                        if not was_voted:
                            candidate = await self.get_candidate(id)
                            if type(candidate) == Candidate:
                                votes = candidate.votes  # type: ignore
                                votes += 1
                                await self.connection.execute("""
                                    DELETE FROM CANDIDATES WHERE id=?
                                """, (id,))
                                await self.connection.execute("""
                                    INSERT INTO CANDIDATES VALUES (?, ?, ?)
                                """, (id, candidate.program, votes))  # type: ignore
                                await self.connection.execute("""
                                    INSERT INTO VOTED VALUES (?, ?)
                                """, (voter_id, id))
                                await self.commit()
                                return 0
                            else:
                                return 1
                        else:
                            return 2
                else:
                    return 3
            else:
                return 4
        else:
            return 5

    async def change_status_of_vote(self, status: Union[int, StatusOfVoting]) -> Optional[Dict[int, Candidate]]:
        await self.connection.execute("""
            DELETE FROM STATUS_OF_VOTE
        """)
        await self.connection.execute("""
            INSERT INTO STATUS_OF_VOTE VALUES (?)
        """, (status,))
        if status == 1:
            candidates = await self.get_all_candidats()
            if type(candidates) == int:
                return
            await self.connection.execute("""
                DELETE FROM VOTED
            """)
            await self.connection.execute("""
                DELETE FROM CANDIDATES
            """)
            await self.commit()
            return candidates  # type: ignore
        else:
            await self.commit()
            return
    
    async def get_status_of_vote(self) -> StatusOfVoting:
        query = await self.connection.execute("""
            SELECT status FROM STATUS_OF_VOTE 
        """)
        if (status := await query.fetchone()):
            return StatusOfVoting(status[0])
        return StatusOfVoting.NO_VOTING
        
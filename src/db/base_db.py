import aiosqlite
import asyncio
import os

class DB:
    def __init__(self) -> None:
        asyncio.get_event_loop().run_until_complete(self.connect())
    
    async def connect(self):
        if not hasattr(self, "connection"):
            self.connection = await aiosqlite.connect("cija.db")

    async def init_tables(self, *args):
        await self.connection.execute("""
            CREATE TABLE IF NOT EXISTS PASSPORTS (
                user_id int,
                name text,
                surname text,
                sex int,
                username text,
                balance int,
                status int,
                job int,
                emoji text DEFAULT '👤',
                partner int DEFAULT 0,
                is_citizen bool,
                passport_photo text,
                birthdate text
            )
        """)
        await self.connection.execute("""
            CREATE TABLE IF NOT EXISTS ADMINS (
                user_id int,
                chat_id int,
                can_mute bool,
                can_ban bool,
                can_pin bool,
                can_manage_money bool,
                can_manage_partyies bool,
                can_give_passports bool,
                can_promote bool
            )
        """)
        await self.connection.execute("""
            CREATE TABLE IF NOT EXISTS PARTYIES (
                party_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                owner INT
            )
        """)
        await self.connection.execute("""
            CREATE TABLE IF NOT EXISTS PARTYIES_MEMBERS (
                party_id int,
                member_id int,
                cam_add_members bool
            )
        """)
        await self.connection.execute("""
            CREATE TABLE IF NOT EXISTS CANDIDATES (
                id int,
                program text,
                votes int
            )
        """)
        await self.connection.execute("""
            CREATE TABLE IF NOT EXISTS VOTED (
                id int,
                vote_for int
            )
        """)
        await self.connection.execute("""
            CREATE TABLE IF NOT EXISTS STATUS_OF_VOTE (
                status int
            )
        """)
        await self.connection.execute("""
            CREATE TABLE IF NOT EXISTS FUNDS (
                fund_id integer primary key autoincrement,
                fund_owner_id int,
                fund_balance int,
                fund_name text
            )
        """)
        await self.connection.execute("""
            CREATE TABLE IF NOT EXISTS FUNDS_PERSONAL (
                fund_id int,
                employee_id int,
                can_withraw bool,
                can_add_personal bool
            )
        """)
        await self.connection.execute("""
            CREATE TABLE IF NOT EXISTS CENTRABANK (
                head int,
                balance int,
                used int
            )
        """)
        await self.connection.execute("""
            CREATE TABLE IF NOT EXISTS CENTRABANK_PERSONAL (
                employee_id int
            )
        """)
        await self.connection.execute("""
            CREATE TABLE IF NOT EXISTS SHOP (
                shop_id INTEGER PRIMARY KEY NOT NULL,
                shop_title text NOT NULL,
                shop_owner_id int NOT NULL,
                default_message text
            )
        """)
        await self.connection.execute("""
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
        await self.connection.execute("""
            CREATE TABLE IF NOT EXISTS BOUGHT_ITEM (
                owner_item_id int NOT NULL,
                item_id INTEGER NOT NULL,
                item_name text NOT NULL,
                description text NOT NULL,
                status text
            )
        """)
        return 0

    async def commit(self):
        await self.connection.commit()
        return
    
    async def close(self, *args):
        await self.commit()
        await self.connection.close()
        os._exit(0)

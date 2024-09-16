import asyncio
import asyncpg
from config import Config

drop_table = """
DROP TABLE IF EXISTS recents;
"""

create_table = """
CREATE TABLE recents (
    account_id bigint,
    ship_id bigint,
    last_battle_time timestamp,
    battles bigint,
    damage_dealt bigint,
    wins bigint,
    xp bigint,
    frags bigint,
    survived_battles bigint,
    shots bigint,
    hits bigint,
    update_at timestamp,
    UNIQUE (account_id, ship_id, last_battle_time)  -- 添加唯一约束
);
"""

total_index = """
CREATE INDEX idx_account_ship_update_time 
ON recents (account_id, ship_id, update_at);
"""

update_at_index = """
CREATE INDEX idx_update_at ON recents(update_at);
"""

# last_battle_time = ship["last_battle_time"]
# battles = pvp["battles"]
# damage_dealt = pvp["damage_dealt"]
# wins = pvp["wins"]
# xp = pvp["xp"]
# frags = pvp["frags"]
# survived_battles = pvp["survived_battles"]
# shots = pvp["main_battery"]["shots"]
# hits = pvp["main_battery"]["hits"]


async def main():
    config = Config()
    async with asyncpg.create_pool(config.psql) as pool:
        async with pool.acquire() as con:
            await con.execute(drop_table)
            await con.execute(create_table)
            await con.execute(total_index)
            await con.execute(update_at_index)
    pass


if __name__ == "__main__":
    asyncio.run(main())

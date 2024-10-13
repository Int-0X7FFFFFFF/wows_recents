from loguru import logger
from token_pool import TokenPool
from config import Config
from collections import defaultdict
import asyncio
from datetime import datetime
from aiowpi import WOWS_ASIA, WOWS_RU, WOWS_EU, WOWS_NA
from connect_pool import DatabasePoll

user_battle_time_cache = defaultdict(int)
paginate = lambda a: map(lambda b: a[b : b + 100], range(0, len(a), 100))

int2server = [
    WOWS_ASIA,
    WOWS_RU,
    WOWS_EU,
    WOWS_NA,
]

config = Config()

async def update_user(token_pool: TokenPool) -> None:
    tasks = []
    
    async with asyncio.TaskGroup() as tg:
        for server, users in enumerate(config.update_users):
            for page in paginate(users):
                logger.debug(page)
                wpi = await token_pool.get()
                tasks.append(
                    (tg.create_task(
                        wpi.player.personal_data(int2server[server], page)
                    ), server)
                )
    update_number = 0
    async with asyncio.TaskGroup() as tg:
        for task, server in tasks:
            if data := await task:
                for user in data:
                    if user:
                        user_id = user["account_id"]
                        last_battle_time = user["last_battle_time"]
                        if user_battle_time_cache[user_id] < last_battle_time:
                            if len(user_battle_time_cache.keys()) > 1000000:
                                user_battle_time_cache.clear()
                            user_battle_time_cache[user_id] = last_battle_time
                            tg.create_task(
                                update_user_ships(token_pool, user_id, server)
                            )
                            update_number += 1
                    else:
                        logger.error(user_id)
    logger.info(f'update user = {update_number}')

async def update_user_ships(
    token_pool: TokenPool, user_id: str, server: int
) -> None:
    wpi = await token_pool.get()  # 从 token 池获取 token 和 session
    data = await wpi.warships.statistics(int2server[server], user_id)

    
    if not data:
        return

    # 获取当前时间戳，作为更新时间
    now = datetime.now()

    pool = DatabasePoll._pool  # 假设你有一个连接池
    async with pool.acquire() as con:
        for ships in data:
            if ships:
                for ship in ships:
                    logger.debug(ship)
                    pvp = ship["pvp"]
                    last_battle_time = datetime.utcfromtimestamp(ship["last_battle_time"])
                    battles = pvp["battles"]
                    damage_dealt = pvp["damage_dealt"]
                    wins = pvp["wins"]
                    xp = pvp["xp"]
                    frags = pvp["frags"]
                    survived_battles = pvp["survived_battles"]
                    shots = pvp["main_battery"]["shots"]
                    hits = pvp["main_battery"]["hits"]
                    ship_id = ship["ship_id"]

                    # 插入或更新数据的 SQL 语句
                    query = """
                    INSERT INTO recents (
                        account_id, ship_id, last_battle_time, battles, damage_dealt, 
                        wins, xp, frags, survived_battles, shots, hits, update_at, server
                    ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13)
                    ON CONFLICT (account_id, ship_id, server, last_battle_time) DO UPDATE SET
                        last_battle_time = EXCLUDED.last_battle_time,
                        battles = EXCLUDED.battles,
                        damage_dealt = EXCLUDED.damage_dealt,
                        wins = EXCLUDED.wins,
                        xp = EXCLUDED.xp,
                        frags = EXCLUDED.frags,
                        survived_battles = EXCLUDED.survived_battles,
                        shots = EXCLUDED.shots,
                        hits = EXCLUDED.hits,
                        update_at = EXCLUDED.update_at;
                    """

                    # 执行 SQL 语句
                    await con.execute(
                        query,
                        int(user_id),           # $1: account_id
                        int(ship_id),           # $2: ship_id
                        last_battle_time,       # $3: last_battle_time
                        battles,                # $4: battles
                        damage_dealt,           # $5: damage_dealt
                        wins,                   # $6: wins
                        xp,                     # $7: xp
                        frags,                  # $8: frags
                        survived_battles,       # $9: survived_battles
                        shots,                  # $10: shots
                        hits,                   # $11: hits
                        now,                    # $12: update_at (当前时间)
                        server,                 # $13: server
                    )

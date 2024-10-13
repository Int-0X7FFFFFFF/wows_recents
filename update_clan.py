from loguru import logger
from token_pool import TokenPool
from config import Config
from aiowpi import WOWS_ASIA, WOWS_EU, WOWS_NA, WOWS_RU

paginate = lambda a: map(lambda b: a[b : b + 100], range(0, len(a), 100))
int2server = [
    WOWS_ASIA,
    WOWS_RU,
    WOWS_EU,
    WOWS_NA,
]

config = Config()

async def update_clan(token_pool: TokenPool) -> None:
    users_tmp = [[], [], [], []]
    wpi = await token_pool.get()
    for server, clans in enumerate(config.update_clans):
        if clans:
            if data := await wpi.clans.details(int2server[server], clans):
                for clan in data:
                    members_ids = clan["members_ids"]
                    users_tmp[server].extend(members_ids)

    # 更新 config 中的用户列表
    config.update_users = users_tmp
    logger.info(
        f"update clan users OK, current_user = {len(users_tmp[0]) + len(users_tmp[1]) + len(users_tmp[2]) + len(users_tmp[3])}"
    )

import logging
from token_pool import TokenPool
from config import Config
from apis import api_get_clan_detail
import asyncio

paginate = lambda a: map(lambda b: a[b : b + 100], range(0, len(a), 100))

logger = logging.getLogger("main")
config = Config()

async def update_clan(token_pool: TokenPool) -> None:
    users_tmp = [[], [], [], []]

    # 使用 TokenPool 获取的 session
    async with asyncio.TaskGroup() as tg:
        for server, clans in enumerate(config.update_clans):
            tasks = []
            for page in paginate(clans):
                # 从 TokenPool 获取 token 和 session
                token, session = await token_pool.get()
                tasks.append(
                    tg.create_task(
                        api_get_clan_detail(session, ",".join(page), server, token)
                    )
                )

            for task in tasks:
                data = await task  # 等待任务完成并获取结果
                if data:
                    for _, clan in data.items():
                        members_ids = clan["members_ids"]
                        users_tmp[server].extend(members_ids)

    # 更新 config 中的用户列表
    config.update_users = users_tmp
    logger.info(
        f"update clan users OK, current_user = {len(users_tmp[0]) + len(users_tmp[1]) + len(users_tmp[2]) + len(users_tmp[3])}"
    )

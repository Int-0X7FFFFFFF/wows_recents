from loguru import logger
import asyncpg
from asyncpg import Pool
from config import Config

config = Config()


class DatabasePoll:
    _pool = None

    def __init__(self) -> None:
        return

    async def __aenter__(self) -> Pool:
        if DatabasePoll._pool == None:
            DatabasePoll._pool = await asyncpg.create_pool(config.psql, max_size=30)
            logger.info("create db connection poll")
        return DatabasePoll._pool

    async def __aexit__(slef, *args) -> None:
        await DatabasePoll._pool.close()
        logger.info("close db connection poll")

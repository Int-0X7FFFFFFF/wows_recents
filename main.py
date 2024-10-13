import time
from clean_old_data import cleanup_old_data
from config import Config
from multiprocessing import Manager
from loguru import logger
import asyncio
from token_pool import TokenPool
from update_clan import update_clan
from update_user import update_user
from connect_pool import DatabasePoll
import sys

config = Config()
logger.add("info_{time}.log", level="INFO", rotation="12:00")
logger.add(sys.stdout, format="{time} - {level} - {message}", filter="sub.module")

@logger.catch
async def main() -> None:
    with Manager() as manager:
        shared_index = manager.Value("i", 0)
        cnt = 0
        try:
            await DatabasePoll().__aenter__()
            token_pool = TokenPool(config.wargaming_tokens, shared_index)
            asyncio.create_task(cleanup_old_data())
            if config.update_by_clan:
                await update_clan(token_pool)
                logger.info("finish clan first update")
            while True:
                try:
                    start_time = time.time()
                    await update_user(token_pool)
                    logger.info('finish, user update')
                    logger.info(f'running time = {time.time() - start_time}')
                finally:
                    cnt = (cnt + 1) % 20
                    if cnt % 20 == 0 and config.update_by_clan:
                        await update_clan(token_pool)
                    await asyncio.sleep(config.running_interval)
        finally:
            await DatabasePoll().__aexit__()


if __name__ == "__main__":
    logger.info("Init")
    asyncio.run(main())

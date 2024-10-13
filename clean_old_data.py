import asyncio
from loguru import logger
import asyncpg
from datetime import datetime, timedelta

from connect_pool import DatabasePoll


async def cleanup_old_data():
    while True:
        # 计算6个月前的时间
        six_months_ago = datetime.now() - timedelta(days=180)

        # 格式化为字符串，适用于SQL查询
        six_months_ago_str = six_months_ago.strftime('%Y-%m-%d %H:%M:%S')

        logger.info(f"Cleaning up records older than {six_months_ago_str}")

        try:
            # 使用 DatabasePoll 连接池执行 SQL 删除操作
            pool = DatabasePoll._pool
            async with pool.acquire() as conn:
                # 删除6个月前的数据
                delete_query = "DELETE FROM recents WHERE update_at < $1"
                await conn.execute(delete_query, six_months_ago)

            logger.info("Cleanup completed successfully.")
        except asyncpg.PostgresError as e:
            logger.error(f"Error during cleanup: {str(e)}")

        # 休眠 24 小时
        await asyncio.sleep(86400)

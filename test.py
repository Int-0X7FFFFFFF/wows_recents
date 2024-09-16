import aiohttp
import asyncio
import time
from asyncio import TaskGroup

wows_account_players_asia = "https://api.worldofwarships.asia/wows/account/list/"
application_id = '339c189eaa59b10856da52149ba71206'

async def api_get_account_id(session: aiohttp.ClientSession, nickName: str) -> dict:
    """
    根据 nickName 获取 account_id (使用亚洲服务器)
    :param session: aiohttp 的 ClientSession
    :param nickName: 游戏内昵称
    :return resp.json: 服务器返回值的 json 转码
    """
    params = [("application_id", application_id), ("search", nickName)]

    async with session.get(wows_account_players_asia, params=params) as resp:
        if resp.status == 200:
            data = await resp.json()
            if data["status"] == "ok":
                return data["data"]
            else:
                raise Exception("参数出现错误")
        else:
            raise Exception("Wargaming 的 API 出现问题/网络出现问题")

async def test_api_rate_limit(nickName: str, max_requests_per_minute: int):
    async with aiohttp.ClientSession() as session:
        while True:
            print(f"\nTesting {max_requests_per_minute} requests per minute...")

            success_count = 0
            error_count = 0
            start_time = time.time()

            # 计算每个请求之间的间隔时间 (单位：秒)
            interval = 60 / max_requests_per_minute

            async def make_request():
                nonlocal success_count, error_count
                try:
                    await api_get_account_id(session, nickName)
                    success_count += 1
                except Exception as e:
                    error_count += 1
                    print(f"Request failed: {e}")

            # 使用 TaskGroup 来管理并发请求
            async with TaskGroup() as tg:
                for i in range(max_requests_per_minute):
                    # 每个请求按时间间隔分散执行
                    tg.create_task(make_request())
                    await asyncio.sleep(interval)

            elapsed_time = time.time() - start_time
            print(f"\nCompleted {max_requests_per_minute} requests in {elapsed_time:.2f} seconds.")
            print(f"Successful requests: {success_count}, Failed requests: {error_count}")

            # 如果没有失败的请求，表示该请求速率稳定，可以提高请求量
            if error_count == 0:
                max_requests_per_minute += 1
                print(f"No errors, increasing request rate to {max_requests_per_minute} requests per minute...")
            else:
                print(f"Error detected at {max_requests_per_minute} requests per minute.")
                break

            # 每次测试完成后等待 1 分钟，以防止结果被影响
            print("Waiting 1 minute before the next test...")
            await asyncio.sleep(60)

        print(f"\nMaximum stable request rate: {max_requests_per_minute - 1} requests per minute.")

# 设置参数并运行测试
nickName = "exboom"  # 替换为你要测试的昵称
max_requests_per_minute = 612  # 设置猜测的一分钟最大访问量

# 运行异步测试
asyncio.run(test_api_rate_limit(nickName, max_requests_per_minute))

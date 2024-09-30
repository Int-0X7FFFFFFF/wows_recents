import aiohttp
from asyncio import Lock
from typing import List
from aiowpi import WPIClient

class TokenPool:
    def __init__(self, tokens: List[str], *args) -> None:
        self.tokens = tokens
        self.token_index = 0
        self.pool_size = len(tokens)
        self.lock = Lock()

        # 为每个 token 创建一个 client
        self.clients = []
        for token in tokens:
            wpi_client = WPIClient(token, 10, 1)
            self.clients.append(wpi_client)

    async def get(self) -> WPIClient:
        async with self.lock:
            # 获取当前 token 和对应的 session
            client = self.clients[self.token_index]

            # 循环更新 token_index，保证轮换使用 token
            self.token_index = (self.token_index + 1) % self.pool_size

            return client
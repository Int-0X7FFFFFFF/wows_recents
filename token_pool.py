import aiohttp
from asyncio import Lock
from typing import List
from asyncio import sleep

class TokenPool:
    def __init__(self, tokens: List[str], *args) -> None:
        self.tokens = tokens
        self.token_index = 0
        self.pool_size = len(tokens)
        self.lock = Lock()

        # 为每个 token 创建一个 session
        self.sessions = []
        for token in tokens:
            connector = aiohttp.TCPConnector(limit=10)
            session = aiohttp.ClientSession(connector=connector)
            self.sessions.append((token, session))

    async def get(self):
        async with self.lock:
            # 获取当前 token 和对应的 session
            token, session = self.sessions[self.token_index]

            # 循环更新 token_index，保证轮换使用 token
            self.token_index = (self.token_index + 1) % self.pool_size

            return token, session

    async def close_sessions(self):
        """关闭所有创建的 ClientSession"""
        for _, session in self.sessions:
            await session.close()
from __future__ import annotations

import asyncio

from .impl.gateway import RevoltGateway 
from .impl.http import HTTPClient
from .impl.dispatcher import Dispatcher


class Client:
    def __init__(self, token: str):
        self.token = token
        self.dispatcher = Dispatcher()
        self.http = HTTPClient()

        self.loop = asyncio.get_event_loop()
    
    
    async def connect(self):
        await self.http.get_api_info()

        while True:
            self.gateway = RevoltGateway(self.dispatcher, self.http)

            await self.gateway.connect()

    async def login(self):
        self.http.login(self.token)

    async def start(self):
        await self.login()
        await self.connect()
    
    async def close(self):
        if not self.gateway or not self.http:
            return

        await self.gateway.close()
        await self.http.session.close()

    def run(self):
        try:
            asyncio.run(self.start())
        except (RuntimeError, KeyboardInterrupt):
            self.loop.run_until_complete(self.close())
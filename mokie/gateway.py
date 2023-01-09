from __future__ import annotations
import asyncio
import json

from typing import TYPE_CHECKING

import logging

from aiohttp import ClientWebSocketResponse, WSMessage, WSMsgType

from .http import HTTPClient

_log = logging.getLogger(__name__)

class Gateway:
    if TYPE_CHECKING:
        ws: ClientWebSocketResponse


    def __init__(self, http: HTTPClient):
        self.http = http
        self.token = self.http.token
        self.loop = asyncio.get_event_loop()

    async def handle_heartbeat(self):
        while True:
            await self.ws.ping()
            await asyncio.sleep(15)

    async def connect(self):
        info = await self.http.get_api_info()

        _log.info(info)

        gateway_url = info["ws"]

        self.ws  = await self.http.session.ws_connect(gateway_url)

        await self.ws.send_json({"type": "Authenticate", "token": self.token})

        asyncio.create_task(self.handle_heartbeat())

        return await self.handle_gateway_events()

    async def handle_gateway_events(self):
        while True:
            msg = await self.ws.receive()

            payload = json.loads(msg.data)

            print(payload["type"])
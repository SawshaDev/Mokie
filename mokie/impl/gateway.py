# MIT License

# Copyright (c) 2023 SawshaDev

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from __future__ import annotations
import asyncio
import json
import traceback

from typing import TYPE_CHECKING

import logging

from aiohttp import ClientWebSocketResponse, WSMessage, WSMsgType

from .http import HTTPClient
from .dispatcher import Dispatcher

_log = logging.getLogger(__name__)


class RevoltGateway:
    if TYPE_CHECKING:
        ws: ClientWebSocketResponse


    def __init__(self, dispatcher: Dispatcher, http: HTTPClient):
        self.http = http
        self.dispatcher = dispatcher
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
        while not self.is_closed:
            msg = await self.ws.receive()

            payload = json.loads(msg.data)
            event_name: str = payload["type"]


            try:
                event = self.dispatcher.event_parsers[event_name.lower()]   
            except Exception as e:
                _log.exception(e)
            else:
                event(payload)

    async def close(self, code: int = 1000):
        await self.ws.close(code=code)
        _log.info("Closing revolt gateway connection")

    @property 
    def is_closed(self) -> bool:
        if not self.ws:
            return True

        return self.ws.closed
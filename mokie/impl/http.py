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

from aiohttp import ClientSession

from typing import Optional, Dict, Any

from urllib.parse import quote as urlquote

from dataclasses import dataclass

DEFAULT_API_URL = "https://api.revolt.chat"


class Route:
    def __init__(self, method: str, url: str, **params: Dict[str, Any]):
        self.method = method
        self.url = url
        self.params = params
    
    @property
    def endpoint(self) -> str:
        """The formatted url for this route."""
        return self.url.format_map(
            {k: urlquote(str(v)) for k, v in self.params.items()}
        )


class HTTPClient:
    def __init__(self, api_url: Optional[str] = None, bot: bool = True):        
        if api_url is not None:
            self.url = api_url
        else:
            self.url = DEFAULT_API_URL

        self.base_headers = {"User-Agent": "Mokie", "Content-Type": "application/json"}
        self.is_bot = bot
        self.api_info: Optional[Dict[str, Any]] = None

    def login(self, token: str):
        self.session = ClientSession()
        self.token = token


    async def request(self, route: Route, auth: Optional[bool] = True, **kwargs) -> Dict[str, Any]: # type: ignore
        token_headers = "x-bot-token" if self.is_bot else "x-session-token"

        if auth:
            self.base_headers[token_headers] = self.token
    
        response = await self.session.request(route.method, f"{self.url}{route.url}", headers=self.base_headers, **kwargs)

        if 200 <= response.status < 300:
            if await response.read() == b"":
                return {}

            return await response.json()

    async def get_api_info(self):
        if self.api_info is not None:
            return self.api_info

        self.api_info = await self.request(Route("GET", ""))

        return self.api_info

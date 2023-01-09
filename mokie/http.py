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
    def __init__(self, session: ClientSession, token: str, *, api_url: Optional[str] = None, bot: bool = True):
        self.token = token
        self.session: ClientSession = session
        
        if api_url is not None:
            self.url = api_url
        else:
            self.url = DEFAULT_API_URL

        self.base_headers = {"User-Agent": "Mokie", "Content-Type": "application/json"}
        self.is_bot = bot
        self.api_info: Optional[Dict[str, Any]] = None


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

from aiohttp import ClientSession

from .gateway import Gateway 
from .http import HTTPClient

class Client:
    def __init__(self, token: str):
        self.token = token
    async def start(self):
        self.session = ClientSession()

        self.http = HTTPClient(self.session, self.token)

        self.gateway = Gateway(self.http)
    
        await self.http.get_api_info()

        await self.gateway.connect()

import bscscan
from aiohttp import ClientSession
from bscscan.core.base import BaseClient
from bscscan.enums.fields_enum import FieldsEnum as fields
from bscscan.utils.parsing import ResponseParser as parser


class AsyncClient(BaseClient):
    async def _build(self):
        for func, v in self._config.items():
            if not func.startswith("_"):  # disabled if _
                attr = getattr(getattr(bscscan, v["module"]), func)
                setattr(self, func, await self._exec(attr))
        return self

    async def _exec(self, func):
        async def wrapper(*args, **kwargs):
            url = (
                f"{self.url}"
                f"{func(*args, **kwargs)}"
                f"{fields.API_KEY}"
                f"{self._api_key}"
            )
            if self._debug:
                print(f"\n{url}\n")
            async with self._session.get(url) as response:
                return parser.parse(await response.json())

        return wrapper

    async def __aenter__(self):
        self._session = ClientSession()
        user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
        self._session.headers.update({'user-agent': user_agent})
        return await self._build()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._session.close()

    @classmethod
    async def from_session(cls, api_key: str, session: ClientSession, **kwargs):
        client = AsyncClient(api_key, **kwargs)
        client._session = session
        return await client._build()

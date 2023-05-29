import bscscan
from bscscan.core.base import BaseClient
from bscscan.enums.fields_enum import FieldsEnum as fields
from bscscan.utils.parsing import ResponseParser as parser
from requests import Session


class SyncClient(BaseClient):
    def _build(self):
        for func, v in self._config.items():
            if not func.startswith("_"):  # disabled if _
                attr = getattr(getattr(bscscan, v["module"]), func)
                setattr(self, func, self._exec(attr))
        return self

    def _exec(self, func):
        def wrapper(*args, **kwargs):
            url = (
                f"{self.url}"
                f"{func(*args, **kwargs)}"
                f"{fields.API_KEY}"
                f"{self._api_key}"
            )
            if self._debug:
                print(f"\n{url}\n")
            with self._session.get(url) as response:
                return parser.parse(response.json())

        return wrapper

    def __enter__(self):
        self._session = Session()
        user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
        self._session.headers.update({'user-agent': user_agent})
        return self._build()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._session.close()

    @classmethod
    def from_session(cls, api_key: str, session: Session, **kwargs):
        client = SyncClient(api_key, **kwargs)
        client._session = session
        return client._build()
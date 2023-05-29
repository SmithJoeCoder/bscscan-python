import json
from importlib import resources

from bscscan import configs
from bscscan.enums.fields_enum import FieldsEnum as fields

CONFIG_FILE = "stable.json"


class BaseClient:
    def __init__(
        self,
        api_key: str,
        is_main_net: bool = True,
        debug: bool = False,  # display generated URLs for debugging purposes
    ):
        self._config = self._load_config()
        self._api_key = api_key
        self._debug = debug
        self.url = fields.PREFIX if is_main_net else fields.TEST_PREFIX
        self.is_main_net = is_main_net

    @staticmethod
    def _load_config(config_file: str = CONFIG_FILE) -> dict:
        with resources.path(configs, config_file) as path, open(path, "r") as f:
            return json.load(f)

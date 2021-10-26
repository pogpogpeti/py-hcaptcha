from typing import Literal
from urllib.parse import urlencode
import json
import time

class Agent:
    def __init__(self):
        self._epoch_delta = 0

    def get_screen_properties(self) -> dict:
        return {}
    
    def get_navigator_properties(self) -> dict:
        return {}

    def epoch(self, ms: int = True):
        t = time.time() * 1000
        t += self._epoch_delta
        if not ms: t /= 1000
        return int(t)

    def epoch_travel(self, delta: float, ms: bool = True):
        if not ms: delta *= 1000
        self._epoch_delta += delta

    def epoch_wait(self):
        if self._epoch_delta > 0:
            time.sleep(self._epoch_delta/1000)
        self._epoch_delta = 0

    def json_encode(self, data: Literal) -> str:
        return json.dumps(data, separators=(",", ":"))

    def url_encode(self, data: dict) -> str:
        return urlencode(data)
    
    def format_headers(
        self,
        url: str,
        headers: dict = {},
        origin_url: str = None,
        sec_site: str = "cross-site",
        sec_mode: str = "cors",
        sec_dest: str = "empty"
    ) -> dict:
        return headers
from __future__ import annotations

from typing import Any

class InstanceInfo:
    __slots__ = (
        "ws",
        "revolt_version",
    )

    def __init__(self, payload: dict[str, Any]):
        self._from_data(payload)

    def _from_data(self, payload: dict[str, Any]) -> None:
        print(payload)
        
        self.ws = payload["ws"]

        self.revolt_version = payload["revolt"]
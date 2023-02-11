from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Any, Callable

import inspect

if TYPE_CHECKING:
    from .impl import HTTPClient

class State:
    def __init__(self, http: HTTPClient):
        self.http = http 
        
    
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
import inspect

from typing import Any, Callable, TypeVar, Coroutine

from collections import defaultdict

import logging



_log = logging.getLogger(__name__)
T = TypeVar("T")
Func = Callable[..., T]
CoroFunc = Func[Coroutine[Any, Any, Any]]


class Dispatcher:
    def __init__(self):
        self.events: dict[str, list[CoroFunc]] = defaultdict(list)
        
        self.event_parsers: dict[str, Callable[[Any], None]] = {}
        for attr, func in inspect.getmembers(self):
            if attr.startswith('parse_'):
                self.event_parsers[attr[6:].lower()] = func

    def add_callback(self, event_name: str, func: CoroFunc):
        self.events[event_name].append(func)

        _log.info("Added callback for %r", event_name)

    def subscribe(self, event_name: str, func: CoroFunc):
        self.add_callback(event_name, func)

        _log.info("Subscribed to %r", event_name)

    def get_event(self, event_name: str):
        return self.events.get(event_name)

    def dispatch(self, event_name: str, *args, **kwargs):
        event = self.get_event(event_name)

        if event is None:
            _log.info("No event for that!")
            return

        for callback in event:
            asyncio.create_task(callback(*args, **kwargs))

        _log.info("Dispatched event %r", event_name)

    def parse_authenticated(self, payload: dict[str, Any]):
        pass

    def parse_ready(self, payload: dict[str, Any]):
        self.dispatch("ready")
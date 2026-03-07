import weakref
from typing import Callable, Dict, Any


class _EventBus:
    def __init__(self):
        self._listeners = {}

    def subscribe(self, event_name: str, callback: Callable[[Dict[str, Any]], None]):
        if not callable(callback):
            raise TypeError("The event callback must be type of Callable.")
        if event_name not in self._listeners:
            self._listeners[event_name] = []
        #
        if hasattr(callback, '__self__'):
            entry = weakref.WeakMethod(callback)
        else:
            entry = lambda: callback
        #
        self._listeners[event_name].append(entry)

    def publish(self, event_name: str, data : Dict[str, Any] = None):
        dead = []
        data = data if data is not None else {}
        for ref in self._listeners.get(event_name, []):
            callback = ref()
            if callback is not None:
                callback(data)
            else:
                dead.append(ref)
        #
        for ref in dead:
            self._listeners[event_name].remove(ref)

    def clear(self):
        self._listeners.clear()


event_bus = _EventBus()
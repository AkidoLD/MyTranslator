

class _EventBus:
    def __init__(self):
        self._listeners = {}

    def subscribe(self, event_name: str, callback):
        if not callable(callback):
            raise TypeError("The event callback must be _type of Callable.")
        #
        if event_name not in self._listeners:
            self._listeners[event_name] = []
        self._listeners[event_name].append(callback)

    def publish(self, event_name: str, data):
        for callback in self._listeners.get(event_name, []):
            callback(data)

    def clear(self):
        self._listeners.clear()


# Globale Instance
event_bus = _EventBus()
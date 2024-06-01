import queue
from typing import Any

class LogQueue:
    def __init__(self) -> None:
        self.queue: queue.Queue = queue.Queue()

    def put(self, log: Any) -> None:
        self.queue.put(log)

    def get(self) -> Any:
        return self.queue.get()

    def empty(self) -> bool:
        return self.queue.empty()
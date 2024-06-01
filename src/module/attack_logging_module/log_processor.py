from typing import List, Dict, TYPE_CHECKING
from threading import Thread
import time
from requests.models import Request
import json

from module.attack_logging_module.log_model import Log
from module.attack_logging_module.enums import HttpMethod

if TYPE_CHECKING:
    from service.connection_service import ConnectionService

from .log_queue import LogQueue

class LogProcessor(Thread):
    def __init__(self, connector: "ConnectionService", log_queue: LogQueue):
        Thread.__init__(self)
        self.connector = connector
        self.log_queue = log_queue
        self.running = True

    def run(self) -> None:
        while self.running:
            logs_to_send = []
            while not self.log_queue.empty():
                logs_to_send.append(self.log_queue.get())

            if logs_to_send:
                self.connector.send_request(*self._map_to_requests(logs_to_send))

            time.sleep(10)  # Wait before checking the queue again

    def stop(self) -> None:
        self.running = False

    def _map_to_requests(self, logs: List[Log]) -> List[Request]:

        requests = []
        for log in logs:
            headers = {"Content-Type": "application/json"}
            request = Request(method = HttpMethod.POST.value,
                              url = self.connector.join_url(self.connector.url, f"api/v1/log/block/{log.log_block_id}/log"),
                              headers = headers, 
                              data = log.to_dict())
            requests.append(request)
        return requests
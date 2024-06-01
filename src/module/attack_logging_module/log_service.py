from .log_model import Log, LogType, LogLevel
from .log_queue import LogQueue

class LoggerService:

    _instance: "LoggerService" = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LoggerService, cls).__new__(cls)
            cls._instance.log_queue = LogQueue()
        return cls._instance

    def debug(self, log_content: str, log_block_id: str, log_type: LogType = LogType.BASIC) -> None:
        self._log(log_content, log_block_id, log_type, LogLevel.DEBUG)

    def info(self, log_content: str, log_block_id: str, log_type: LogType = LogType.BASIC) -> None:
        self._log(log_content, log_block_id, log_type, LogLevel.INFO)

    def warn(self, log_content: str, log_block_id: str, log_type: LogType = LogType.BASIC) -> None:
        self._log(log_content, log_block_id, log_type, LogLevel.WARN)

    def error(self, log_content: str, log_block_id: str, log_type: LogType = LogType.BASIC) -> None:
        self._log(log_content, log_block_id, log_type, LogLevel.ERROR)

    def critical(self, log_content: str, log_block_id: str, log_type: LogType = LogType.BASIC) -> None:
        self._log(log_content, log_block_id, log_type, LogLevel.CRITICAL)

    def log_data(self, log_content:str, log_block_id: str, log_type: LogType = LogType.INFORMATION) -> None:
        self._log(log_content, log_block_id, log_type, LogLevel.INFO)

    @classmethod
    def get_logger(cls):
        return cls()

    def _log(self, 
             log_content: str,
             log_block_id: str,
             log_type: LogType, 
             log_level: LogLevel) -> None:
        log_entry = Log(log_content, log_block_id, log_type, log_level)
        self.log_queue.put(log_entry)
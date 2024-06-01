
from module.attack_logging_module.enums import LogType, LogLevel 

import uuid

class Log:
    def __init__(self, log_content: str, log_block_id: str , log_type: LogType, log_level: LogLevel):
        self.log_content = log_content
        self.log_block_id = log_block_id
        self.log_type = log_type
        self.log_level = log_level

    def to_dict(self):
        return {
            "log_text": self.log_content,
            "log_type": self.log_type.name,
            "log_level": self.log_level.name
        }
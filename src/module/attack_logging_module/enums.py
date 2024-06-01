
from enum import Enum

class HttpMethod(Enum):
    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'
    DELETE = 'DELETE'

class LogType(Enum):
    BASIC = "basic"
    INFORMATION = "information"

class LogLevel(Enum):
    DEBUG = "debug"
    INFO = "info"
    WARN = "warn"
    ERROR = "error"
    CRITICAL = "critical"
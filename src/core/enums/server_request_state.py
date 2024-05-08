from enum import Enum

from core.decorators.enum_decorators import from_string

@from_string
class ServerRequestState(Enum):
    WORKING = "working"
    CLOSED = "closed"
    DEBUGGING = "debugging"
    INTERNAL_ERROR = "internal_error"
    CRASHED = "crashed"
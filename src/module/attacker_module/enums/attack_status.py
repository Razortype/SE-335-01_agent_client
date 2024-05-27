
from enum import Enum

class AttackStatus(Enum):

    IDLE = "idle",
    EXECUTING = "executing",
    DONE = "done",
    CRASHED = "crashed"
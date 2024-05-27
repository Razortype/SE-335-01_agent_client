
from enum import Enum

from core.decorators.enum_decorators import from_string

@from_string
class AttackType(Enum):
    COOKIE_DISCOVERY = "cookie_discovery"
    FILE_FOLDER_DISCOVERY = "file_folder_discovery"
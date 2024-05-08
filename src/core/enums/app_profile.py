
from enum import Enum

from core.decorators.enum_decorators import from_string

@from_string
class AppProfile(Enum):
    DEV = "dev"
    PRODUCT = "product"
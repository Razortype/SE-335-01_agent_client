
from enum import Enum

from core.decorators.enum_decorators import from_string

@from_string
class MessageType(Enum):
    
    AGENT_INFO_PACKAGE = "agent_info_package"
    AGENT_INIT_PACKAGE = "agent_init_package"
    ATTACK_PACKAGE = "attack_package"
    ATTACK_CONF_PACKAGE = "attack_conf_package"
    MANAGER_AGENT_INFO_PACKAGE = "manager_agent_info_package"
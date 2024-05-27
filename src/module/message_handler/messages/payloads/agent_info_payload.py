
from dataclasses import dataclass
from typing import List, Optional
from module.message_handler.messages.payloads.base_payload import BasePayload
from module.message_handler.messages.payloads.attack_payload import AttackPayload
from core.enums.agent_status import AgentStatus

@dataclass
class AgentInformationPayload(BasePayload):
    agent_status: AgentStatus
    executing_attack: Optional[AttackPayload]
    amount_of_queued_attack: int
    using_token: str
    execution_history: List[AttackPayload]

    def to_dict(self):
        dict_rep = super().to_dict()
        
        dict_rep["agent_status"] = self.agent_status.name
        dict_rep["executing_attack"] = self.executing_attack.to_dict() if self.executing_attack else None
        dict_rep["amount_of_queued_attack"] = self.amount_of_queued_attack
        dict_rep["using_token"] = self.using_token
        dict_rep["execution_history"] = [i.to_dict() for i in self.execution_history]
        
        return dict_rep
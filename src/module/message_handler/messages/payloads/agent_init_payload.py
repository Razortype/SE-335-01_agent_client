
from dataclasses import dataclass
from datetime import datetime
from uuid import UUID
from module.message_handler.messages.payloads.base_payload import BasePayload

@dataclass
class AgentInitializationPayload(BasePayload):
    agent_email: str
    connected_at: datetime

    def to_dict(self):
        dict_rep = super().to_dict()
        dict_rep.update({
                "agent_email": self.agent_email,
                "connected_at": self.format_datetime(self.connected_at)})
        return dict_rep
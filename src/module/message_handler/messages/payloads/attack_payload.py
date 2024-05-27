
from dataclasses import dataclass
from typing import Optional
from datetime import datetime
from uuid import UUID

from module.attacker_module.enums.attack_type import AttackType
from module.message_handler.messages.payloads.base_payload import BasePayload

@dataclass
class AttackPayload(BasePayload):
    attack_job_id: UUID
    log_block_id: UUID
    attack_name: str
    attack_description: str
    attack_type: AttackType
    executed_at: datetime

    def to_dict(self):
        dict_rep = super().to_dict()
        dict_rep.update({
            "attack_job_id": str(self.attack_job_id),
            "log_block_id": str(self.log_block_id),
            "attack_name": self.attack_name,
            "attack_description": self.attack_description,
            "attack_type": self.attack_type.name,
            "executed_at": self.format_datetime(self.executed_at)})
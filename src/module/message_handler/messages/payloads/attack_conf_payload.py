
from dataclasses import dataclass
from datetime import datetime
from uuid import UUID
from module.attacker_module.enums.attack_status import AttackStatus
from module.message_handler.messages.payloads.base_payload import BasePayload

@dataclass
class AttackConfirmationPayload(BasePayload):
    attack_job_id: UUID
    attack_status: AttackStatus
    start_executing_at: datetime

    def to_dict(self):
        dict_rep = super().to_dict()
        dict_rep.update({
            "attack_job_id": str(self.attack_job_id),
            "attack_status": self.attack_status,
            "start_executing_at": self.format_datetime(self.start_executing_at)})
        return dict_rep
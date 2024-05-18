
from uuid import UUID
from datetime import date

from module.attacker_module.enums.attack_type import AttackType

class AttackPackage:
    
    def __init__(self,
                 attack_job_id: UUID,
                 attack_name: str,
                 attack_description: str,
                 attack_type: AttackType,
                 executed_at: date,
                 log_block_id: UUID
                 ) -> None:
        self.attack_job_id = attack_job_id
        self.attack_name = attack_name
        self.attack_description = attack_description
        self.attack_type = attack_type
        self.executed_at = executed_at
        self.log_block_id = log_block_id

    @classmethod
    def from_response(cls) -> "AttackPackage" | None:
        # gather parameter
        # parse parameters
        # create instance
        # return instance
        # incase of error return None
        return
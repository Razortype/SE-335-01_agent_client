
from abc import ABC, abstractmethod

from module.attacker_module.enums.attack_status import AttackStatus

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from module.attacker_module.attack_executor import AttackExecutor

class IAttack:

    @abstractmethod
    def attack(self):
        """"""

    @abstractmethod
    def job(self):
        """"""

class Attack(IAttack):

    def __init__(self, executor: "AttackExecutor", attack_payload) -> None:
        self.executor = executor
        self.attack_payload = attack_payload
    
    def attack(self):
        self.executor._attack_status = AttackStatus.EXECUTING
        
        try:
            self.job()
        except Exception as e:
            print("UEO: " + e)

        self.executor._attack_status = AttackStatus.DONE
    
    def job(self):
        raise NotImplementedError("Attack.job() not implemented!")

from abc import ABC, abstractmethod

class IAttack:

    @abstractmethod
    def attack(self):
        """"""

class Attack:
    
    def attack(self):
        raise NotImplementedError("Attack.attack() not implemented!")
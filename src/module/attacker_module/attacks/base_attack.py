
from abc import ABC, abstractmethod

class IAttack:

    @abstractmethod
    def attack(self):
        """"""

    @abstractmethod
    def attack_helper_function(self):
        """"""

class Attack(IAttack):
    
    def attack(self):
        raise NotImplementedError("Attack.attack() not implemented!")
    
    def attack_helper_function(self):
        # code your function here
        pass
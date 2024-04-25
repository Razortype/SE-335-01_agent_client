
from typing import List
import time
from threading import Thread

from module.attacker_module.attacks.base_attack import Attack

class AttackExecutor:

    def __init__(self) -> None:
        
        self.attack_pool: List[Attack] = []
        self.selected_attack: Attack = None

        self.running = False
        self.executor_thread = None

        self.pool_click = 3

    def start(self):
        self.running = True
        self.executor_thread = Thread(target=self.pool_executor, daemon=True)
        self.executor_thread.start()

    def stop(self):
        self.running = False
        self.executor_thread.join()
        self.executor_thread = None

    def set_attack(self, attack: Attack) -> None:
        self.selected_attack = attack

    def add_attack(self, attack: Attack):
        self.attack_pool.append(attack)

    def remove_attack(self, attack: Attack) -> None:
        self.attack_pool.remove(attack)

    def pool_executor(self):
        
        while self.running:

            if self.selected_attack is not None:
                self.selected_attack.attack()
                self.remove_attack()
            else:
                print("No attack set!!")

            time.sleep(self.pool_click)
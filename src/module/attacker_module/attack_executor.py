from typing import List, Optional, TYPE_CHECKING
import time
from threading import Thread, Event

from module.attacker_module.attacks.base_attack import Attack
from core.enums.server_request_state import ServerRequestState

if TYPE_CHECKING:
    from core.app import App

class AttackExecutor:
    def __init__(self, app: "App") -> None:
        self.app = app
        self.attack_pool: List[Attack] = []
        self.selected_attack: Optional[Attack] = None
        self.running = Event()
        self.executor_thread: Optional[Thread] = None
        self.pool_click = 3

    def start(self):
        self.running.set()
        self.executor_thread = Thread(target=self.pool_executor, daemon=True)
        self.executor_thread.start()

    def stop(self):
        self.running.clear()
        if self.executor_thread is not None:
            self.executor_thread.join()
            self.executor_thread = None

    def set_attack(self, attack: Attack) -> None:
        self.selected_attack = attack

    def add_attack(self, attack: Attack):
        self.attack_pool.append(attack)

    def remove_attack(self, attack: Attack) -> None:
        if attack in self.attack_pool:
            self.attack_pool.remove(attack)

    def pool_executor(self):
        while self.running.is_set():
            if self.app.server_status == ServerRequestState.WORKING:
                if self.selected_attack is not None:
                    self.selected_attack.attack()
                    self.selected_attack = None
            time.sleep(self.pool_click)
    
    def print_state(self):
        """Prints the current state of the attack executor."""
        print("~~ ATTACK EXECUTOR STATE ~~")
        print(f"Running: {self.running.is_set()}")
        print(f"Selected Attack: {self.selected_attack}")
        print(f"Attack Pool: {self.attack_pool}")
        print(f"Executor Thread: {self.executor_thread}")
        print(f"Pool Click: {self.pool_click}")
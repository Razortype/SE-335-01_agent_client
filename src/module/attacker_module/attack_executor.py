from typing import List, Optional, TYPE_CHECKING
import time
from threading import Thread, Event
from uuid import UUID

from module.attacker_module.attacks.base_attack import Attack
from module.attacker_module.attacks.custom_attack import CookieAttack, FileFolderDiscoveryAttack
from module.attacker_module.enums.attack_type import AttackType
from module.attacker_module.enums.attack_status import AttackStatus
from module.message_handler.messages.payloads.attack_payload import AttackPayload

from core.enums.server_request_state import ServerRequestState
from core.enums.agent_status import AgentStatus


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
        self._attack_status: AttackStatus = None
        self._attack_history: List[Attack] = []

    def start(self):
        self.running.set()
        self.executor_thread = Thread(target=self.pool_executor, daemon=True)
        self.executor_thread.start()
        self._attack_status = AttackStatus.IDLE

    def stop(self):
        self.running.clear()
        if self.executor_thread is not None:
            self.executor_thread.join()
            self.executor_thread = None

    def submit_attack(self, payload: AttackPayload):
        
        if self.check_payload_exist(payload.attack_job_id):
            print("Attack already exist: " + str(payload.attack_job_id))
            return

        attack: Attack
        if payload.attack_type == AttackType.COOKIE_DISCOVERY:
            attack = CookieAttack(self, payload)
        elif payload.attack_type == AttackType.FILE_FOLDER_DISCOVERY:
            attack = FileFolderDiscoveryAttack(self, payload)
        else:
            print("Invalid Attack Type")

        self.add_attack(attack)

    def set_attack(self, attack: Attack) -> None:
        self.selected_attack = attack

    def add_attack(self, attack: Attack):
        # create attack and initialize here
        self.attack_pool.append(attack)

    def remove_attack(self, attack: Attack) -> None:
        if attack in self.attack_pool:
            self.attack_pool.remove(attack)

    def pick_attack(self):

        if self._attack_status == AttackStatus.DONE:
            self._attack_history.append(self.selected_attack)
            self.selected_attack = None
            self._attack_status = AttackStatus.IDLE

        if self._attack_status != AttackStatus.IDLE: 
            return
        
        if self.attack_pool and self.selected_attack == None:
            self.selected_attack = self.attack_pool.pop(0)
            self.app.confirm_attack(self.selected_attack)

    def pool_executor(self):
        while self.running.is_set():
            
            if self.app.server_status == ServerRequestState.WORKING and self.app._agent_status == AgentStatus.IDLE:
                
                self.pick_attack()
                
                if self.selected_attack is not None:
                    self.selected_attack.attack()
                         
            time.sleep(self.pool_click)
    
    def print_state(self):
        """Prints the current state of the attack executor."""
        print("~~ ATTACK EXECUTOR STATE ~~")
        print(f"Running: {self.running.is_set()}")
        print(f"Selected Attack: {self.selected_attack}")
        print(f"Attack Pool: {self.attack_pool}")
        print(f"Executor Thread: {self.executor_thread}")
        print(f"Pool Click: {self.pool_click}")

    def get_current(self):
       return self.selected_attack
    
    def get_queue_len(self):
        return len(self.attack_pool)
    
    def get_execution_history(self):
        return self._attack_history
    
    def check_payload_exist(self, attack_job_id: UUID):
        
        ids = []
        if (self.selected_attack):
            ids.append(self.selected_attack.attack_payload.attack_job_id)
        for attack in self.attack_pool:
            ids.append(attack.attack_payload.attack_job_id)
        
        return attack_job_id in ids
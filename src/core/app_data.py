
from platformdirs import user_cache_dir
from pathlib import Path
import pickle
import os

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.app import App

class AppData:

    def __init__(self, 
                 email: str, 
                 password: str) -> None:
        self.email = email
        self.password = password

class AppDataManager:
    
    cache_path = Path(user_cache_dir("agentapp", "cache"))
    cache_dir = cache_path / "app"

    cache: AppData = None

    @classmethod
    def get_cache(cls) -> AppData:
        if cls.cache is None:
            cls.insert_cache()
        return cls.cache

    @classmethod
    def set_cache(cls, app_data: AppData) -> None:
        cls.app_data = app_data
        cls.deploy_cache(app_data)

    @classmethod
    def deploy_cache(cls, app_data: AppData):
        
        if not os.path.isdir(cls.cache_path):
            os.makedirs(cls.cache_path)
        
        with open(cls.cache_dir, "wb") as file:
            pickle.dump(app_data, file)

    @classmethod
    def insert_cache(cls) -> None:
        with open(cls.cache_dir, "rb") as file:
            app_data: AppData = pickle.load(file)
        cls.cache = app_data

    @classmethod
    def is_cache_exist(cls) -> bool:
        return os.path.exists(cls.cache_dir)
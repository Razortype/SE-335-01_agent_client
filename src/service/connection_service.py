
import requests
from requests import Response
from typing import List, TYPE_CHECKING

from core.app_data import AppDataManager, AppData

from service.tools.app_decorator import authorized

import jwt

if TYPE_CHECKING:
    from core.app import App

class ConnectionService:
    
    AUTH_PATH = "api/v1/auth/authenticate"
    REFRESH_PATH = "api/v1/auth/refresh"

    def __init__(self,
                 url: str) -> None:
        self.url = url

        self.access_token = None
        self.headers = {}
        self.cookies = None

    @authorized
    def validate_agent(self, email: str = "", password: str = "") -> bool:

        res = self.login(email, password)
        return res.ok
    

    def login(self, email: str = "", password: str = ""):

        auth_url = self.join_url(self.url, self.AUTH_PATH)

        app_data = AppDataManager.get_cache()

        if app_data is not None:
            email = app_data.email
            password = app_data.password

        res = requests.post(
            url=auth_url,
            json={"email": email,
                  "password": password}
        )

        if res.status_code == 200:
            self.set_login(res)
            AppDataManager.set_cache(
                AppData(email, password))
    
        return res

    def refresh(self):
        
        refresh_url = self.join_url(self.url, self.REFRESH_PATH)

        res = requests.post(
            url=refresh_url,
            cookies=self.cookies)

        if not res.ok:
            print("refresh Error")
            self.login()

        self.set_login(res)

    def decode_jwt(self, 
                   token: str) -> dict:

        try:
            decoded_token = jwt.decode(token, algorithms=['none'])
            print(decoded_token)
        except jwt.ExpiredSignatureError:
            print("Token has expired")
            self.refresh()
        except jwt.InvalidTokenError:
            print("Invalid token")
            raise RuntimeError("Invalid Token")

    def set_login(self, res: Response) -> None:

        if res.status_code == 200:
            self.access_token = res.json().get("access_token", None)
            self.cookies = res.cookies
            self.headers["Authorization"] = f"Bearer {self.access_token}"

    @staticmethod
    def join_url( *args: List[str]) -> str:
        return "/".join(args)
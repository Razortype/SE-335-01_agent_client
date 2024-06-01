import requests
from requests import Request
from requests import Response
from typing import List, TYPE_CHECKING
import jwt

from core.app_data import AppDataManager, AppData
from core.enums.server_request_state import ServerRequestState

if TYPE_CHECKING:
    from core.app import App

class ConnectionService:
    
    AUTH_PATH = "api/v1/auth/authenticate"
    REFRESH_PATH = "api/v1/auth/refresh"
    SERVER_STATE_PATH = "api/v1/server/state"

    def __init__(self, app: "App", url: str) -> None:
        self.app = app
        self.url = url
        self._access_token = None
        self.headers = {}
        self.cookies = None
    
    @property
    def access_token(self):
        """Getter for access_token."""
        return self._access_token

    @access_token.setter
    def access_token(self, value):
        """Setter for access_token."""
        # You can add validation logic here if needed
        self._access_token = value


    def get_server_status(self):
        try:
            response = requests.get(self.join_url(self.url, self.SERVER_STATE_PATH))
            if response.status_code != 200:
                raise RuntimeError("Error Response: " + str(response.json()))
            return ServerRequestState.from_string(response.json().get("data").get("server_state"))
        except requests.RequestException:
            return ServerRequestState.CLOSED
        except Exception as e:
            print("Server exception error:", e)
            self.print_state()
            return ServerRequestState.CRASHED

    def validate_agent(self, email: str = "", password: str = "") -> bool:
        res = self.login(email, password)
        return res.ok

    def login(self, email: str = "", password: str = ""):
        auth_url = self.join_url(self.url, self.AUTH_PATH)
        app_data = AppDataManager.get_cache()
        if app_data is not None:
            email = app_data.email
            password = app_data.password
        res = requests.post(url=auth_url, json={"email": email, "password": password})
        if res.status_code == 200:
            self.set_login(res)
            AppDataManager.set_cache(AppData(email, password))
        return res

    def refresh(self):
        refresh_url = self.join_url(self.url, self.REFRESH_PATH)
        res = requests.post(url=refresh_url, cookies=self.cookies)
        if not res.ok:
            print("refresh Error")
            self.login()
        self.set_login(res)

    def decode_jwt(self, token: str) -> dict:
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
            self._access_token = res.json().get("access_token", None)
            self.cookies = res.cookies
            self.headers["Authorization"] = f"Bearer {self._access_token}"

    def send_request(self, *requests_queue: List[Request], auth = True):
        for request in requests_queue:
            try:
                self._set_request_init(request)
                if auth:
                    request.headers.update(self.headers)

                response = requests.request(request.method, request.url, headers=request.headers, json=request.data)
                if response.status_code != 200:
                    print("Error: " + response.text)

            except Exception as e:
                print(f"Error sending request to {request.url}: {e}")
    
    def _set_request_init(self, request: Request):

        if not request.data:
            request.data = {}
        if not request.headers:
            request.headers = {}

    def print_state(self):
        """Prints the current status of the connection."""
        print("~~ CONNECTION SERVICE STATE ~~")
        print(f"URL: {self.url}")
        print(f"Access Token: {self._access_token}")
        print(f"Headers: {self.headers}")
        print(f"Cookies: {self.cookies}")

    @staticmethod
    def join_url(*args: List[str]) -> str:
        return "/".join(args)
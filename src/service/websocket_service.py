import websocket
import threading
import time
import json

from module.message_handler.message_factory import MessageFactory

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.app import App

class WebSocketClientSevice:
    def __init__(self, app: "App", url: str, path: str):
        
        self.app = app
        self.url = url
        self.path = path

        self.connection_url = self.url + self.path

        self.ws = None
        self.thread = None
        self.is_connected = False

    def connect(self):
        # Create a custom HTTP header containing the authorization token
        headers = {"Authorization": f"Bearer {self.app._connection_service.access_token}"}
        
        # Pass the headers to the WebSocketApp constructor
        self.ws = websocket.WebSocketApp(self.connection_url,
                                          header=headers,
                                          on_open=self.on_open,
                                          on_message=self.on_message,
                                          on_error=self.on_error,
                                          on_close=self.on_close)
        
        # Start the WebSocket connection in a separate thread
        self.thread = threading.Thread(target=self.ws.run_forever)
        self.thread.daemon = True
        self.thread.start()

    def disconnect(self):

        if not self.is_connected:
            print("Not connected to WebSocket server")
            return
        
        self.ws.close()
        self.thread.join()
        self.thread = None
        self.is_connected = False

    def on_open(self, ws):
        print("Socket: Agent Connected to Server")
        self.is_connected = True
        self.app.send_app_init_data()

    def on_message(self, ws, message):
        print(message)
        conv_message = MessageFactory.parse_custom_message(message)
        if not conv_message:
            print("Received Message Invalid")
            return

        self.app.handle_message(conv_message)

    def on_error(self, ws, error):
        print(f"Error: {error}")

    def on_close(self, ws, close_status_code, close_reason):
        print("Connection closed")
        self.disconnect()

    def send_message(self, message):
        
        if not self.connect:
            print("Not connected to WebSocket server")
            return

        self.ws.send(message)
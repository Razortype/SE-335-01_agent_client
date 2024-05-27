
from datetime import datetime
from uuid import UUID
from typing import TypeVar, Generic

from module.message_handler.enums.message_type import MessageType

T = TypeVar('T')

class CustomMessage(Generic[T]):
    def __init__(self, message_id: UUID, message: str, message_type: MessageType, creation_date: datetime, payload: T):
        self.message_id = message_id
        self.message = message
        self.message_type = message_type
        self.creation_date = creation_date
        self.payload = payload

    def to_dict(self):
        return {
            "message_id": str(self.message_id),
            "message": self.message,
            "message_type": self.message_type.name,
            "creation_date": self.format_datetime(self.creation_date),
            "payload": self.payload.to_dict()
        }
    
    @staticmethod
    def format_datetime(dt: datetime):
        return dt.strftime('%Y-%m-%dT%H:%M:%S')
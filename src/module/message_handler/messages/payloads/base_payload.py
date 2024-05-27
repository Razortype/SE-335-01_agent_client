from dataclasses import dataclass
from uuid import UUID
from typing import Optional
from datetime import datetime

@dataclass
class BasePayload:
    payload_id: Optional[UUID]

    def to_dict(self):
        return {"payload_id": str(self.payload_id)}
    
    @staticmethod
    def format_datetime(dt: datetime):
        return dt.strftime('%Y-%m-%dT%H:%M:%S')
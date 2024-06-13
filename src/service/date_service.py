
from datetime import datetime
import pytz

class DateService:

    local_timezone = pytz.timezone("Europe/Istanbul")

    @classmethod
    def now(cls) -> datetime:
        now_utc = datetime.now(pytz.utc)
        now_local = now_utc.astimezone(cls.local_timezone)
        return now_local
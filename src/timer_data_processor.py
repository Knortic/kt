import json

from datetime import datetime, timedelta

from src.generator import IDataGenerator
from src.writer import IWriter
from src.errors import InvalidArgumentError
from src.timer_data import TimerData

class JsonTimerDataProcessor():
    def remove_timer_entry_by_id(self, data, timer_id):
        if not isinstance(data, list):
                raise InvalidArgumentError("Provided data was invalid!")
        
        for idx, obj in enumerate(data):
            if obj["id"] == timer_id:
                data.pop(idx)
                return

        raise InvalidArgumentError("Failed to locate data to remove!")


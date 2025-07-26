from datetime import datetime, timedelta

from src.generator import IDataGenerator
from src.writer import IWriter
from src.errors import InvalidArgumentError

class TimerData:
    def __init__(self, timestamp, message, duration):
        self.timestamp = timestamp
        self.message = message
        self.duration = duration

class JsonTimerDataGenerator(IDataGenerator):
    def __init__(self, timer_data):
        self.timer_data = timer_data

    def generate_data_from_existing(self, data):
        if not isinstance(data, list):
            raise InvalidArgumentError("Provided data was invalid!")

        if self.timer_data.timestamp is None:
            raise InvalidArgumentError("Invalid timestamp within timer data!")
        elif not isinstance(self.timer_data.message, str):
            raise InvalidArgumentError("Invalid message within timer data!")
        elif not isinstance(self.timer_data.duration, str):
            raise InvalidArgumentError("Invalid duration within timer data!")

        # We compute the latest_id by first getting the length of the items
        # in the json data and then substracting one to convert it to index-based
        latest_id = len(data) - 1

        self.json_obj = data
        self.json_obj.append({})

        # Since this is the next item we are generating we need to add one
        # otherwise the latest id will point to the previous item and not the new
        # item we are generating
        self.json_obj[-1]["id"] = latest_id + 1;

        self.json_obj[-1]["paused"] = False;
        self.json_obj[-1]["reset"] = False;

        self.json_obj[-1]["message"] = self.timer_data.message;
        self.json_obj[-1]["duration"] = self.timer_data.duration;

        self.json_obj[-1]["timestamp"] = self.timer_data.timestamp.isoformat();

    def generate_data(self):
        self.json_obj = []
        self.generate_data_from_existing(self.json_obj)


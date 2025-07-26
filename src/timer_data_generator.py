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

    def generate_data(self):
        self.json_obj = []
        self.json_obj.append({})

        if self.timer_data.timestamp is None:
            raise InvalidArgumentError("Invalid timestamp within timer data!")
        elif not isinstance(self.timer_data.message, str):
            raise InvalidArgumentError("Invalid message within timer data!")
        elif not isinstance(self.timer_data.duration, str):
            raise InvalidArgumentError("Invalid duration within timer data!")

        # This is generating the data for the first time so hard-coding id of 0
        # is intentional
        self.json_obj[0]["id"] = 0;

        # This is generating the data for the first time so hard-coding 'False'
        # is intentional
        self.json_obj[0]["paused"] = False;
        # This is generating the data for the first time so hard-coding 'False'
        # is intentional
        self.json_obj[0]["reset"] = False;

        self.json_obj[0]["message"] = self.timer_data.message;
        self.json_obj[0]["duration"] = self.timer_data.duration;



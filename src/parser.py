from datetime import datetime, timedelta

class InvalidArgumentError(Exception):
    pass

MAX_ARGS = 2

class TimeStamp:
    def __init__(self, future_timestamp):
        self.current_timestamp = datetime.now()
        self.date = self.current_timestamp + future_timestamp 

class CommandLineArgsParser:
    def __init__(self, *args):
        self.args = list(args)

    def process_args(self):
        has_too_many_args = len(self.args) > MAX_ARGS
        if has_too_many_args:
            raise InvalidArgumentError("Arguments exceeded size of 2!")

        duration = self.args[0]

        is_minute_format = duration.endswith('m')

        if is_minute_format:
            duration = duration[:-1]
            self.args[0] = duration

        if not (duration.isnumeric()):
            raise InvalidArgumentError("Invalid first argument, must be numeric!")
        elif (int(duration) < 0):
            raise InvalidArgumentError("Specified duration cannot be negative!")

        if is_minute_format:
            self.out_timestamp = TimeStamp(timedelta(minutes=int(duration)))
            print(self.out_timestamp.date)

        description = self.args[1]

        if not isinstance(description, str):
            raise InvalidArgumentError("Invalid second argument, must be of type string!")

        return self.args

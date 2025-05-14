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

    def is_second_format(self, input_str):
        return input_str.endswith('s')

    def is_minute_format(self, input_str):
        return input_str.endswith('m')

    def is_hour_format(self, input_str):
        return input_str.endswith('h')

    def has_any_time_format(self, input_str):
        format_match_count = 0

        if self.is_second_format(input_str):
            format_match_count += 1
        elif self.is_minute_format(input_str):
            format_match_count += 1
        elif self.is_hour_format(input_str):
            format_match_count += 1

        return format_match_count > 0

    def convert_to_duration_string(self, input_str):
        if self.has_any_time_format(input_str):
            # Trim the last character off the string
            input_str = input_str[:-1]

        return input_str

    def process_args(self):
        has_too_many_args = len(self.args) > MAX_ARGS
        if has_too_many_args:
            raise InvalidArgumentError("Arguments exceeded size of 2!")

        raw_duration = self.args[0]

        is_second_format = self.is_second_format(raw_duration)
        is_minute_format = self.is_minute_format(raw_duration)
        is_hour_format = self.is_hour_format(raw_duration)

        self.args[0] = self.convert_to_duration_string(raw_duration)
        duration = self.args[0]

        if not (duration.isnumeric()):
            raise InvalidArgumentError("Invalid first argument, must be numeric!")
        elif (int(duration) < 0):
            raise InvalidArgumentError("Specified duration cannot be negative!")

        if is_second_format:
            self.out_timestamp = TimeStamp(timedelta(seconds=int(duration)))

        if is_minute_format:
            self.out_timestamp = TimeStamp(timedelta(minutes=int(duration)))

        if is_hour_format:
            self.out_timestamp = TimeStamp(timedelta(hours=int(duration)))

        description = self.args[1]

        if not isinstance(description, str):
            raise InvalidArgumentError("Invalid second argument, must be of type string!")

        return self.args

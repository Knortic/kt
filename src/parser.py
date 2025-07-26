from datetime import datetime, timedelta

from src.errors import InvalidArgumentError

class TimeStamp:
    def __init__(self, future_timestamp):
        self.current_timestamp = datetime.now()
        self.date = self.current_timestamp + future_timestamp 

class ParsedCommand:
    def __init__(self, timestamp, message):
        self.timestamp = timestamp
        self.message = message

# TODO: Add ability to do days, maybe even months
# TODO: Add ability to parse more complicated time durations e.g. 1 hour 20 minutes 30 seconds:
#   kt add -m "test" -t "1h20m30s"
#   kt add -m "test" -t "1h 20m 30s"
#   kt add -m "test" -t "1h;20m;30s"
# Decide on a suitable format...

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
        arg_count = len(self.args)

        # Required argument count is either 2 or 4 because the format is as follows:
        # 2: "-t" "20s"
        # 4: "-m" "Message here" "-t" "20s"
        has_invalid_arg_count = arg_count != 2 and arg_count != 4
        if has_invalid_arg_count:
            raise InvalidArgumentError("Invalid argument count provided!")

        if arg_count == 2:
            if self.args[0] != "-t":
                raise InvalidArgumentError("Provided invalid first argument, expected '-t'")
        else:
            if self.args[0] != "-m":
                raise InvalidArgumentError("Provided invalid first argument, expected '-m'")

        # To grab the duration we can just get the last argument since if correct arguments were provided then it is the last argument in the list
        raw_duration = self.args[-1]

        self.args[-1] = self.convert_to_duration_string(raw_duration)
        duration = self.args[-1]

        if not (duration.isnumeric()):
            raise InvalidArgumentError("Specified duration must be numeric!")
        elif (int(duration) < 0):
            raise InvalidArgumentError("Specified duration cannot be negative!")

        is_second_format = self.is_second_format(raw_duration)
        is_minute_format = self.is_minute_format(raw_duration)
        is_hour_format = self.is_hour_format(raw_duration)

        out_timestamp = None

        if is_second_format:
            out_timestamp = TimeStamp(timedelta(seconds=int(duration)))

        if is_minute_format:
            out_timestamp = TimeStamp(timedelta(minutes=int(duration)))

        if is_hour_format:
            out_timestamp = TimeStamp(timedelta(hours=int(duration)))

        parsed_cmd = ParsedCommand(out_timestamp, "")

        # No message was provided if the args count is 2 so we can just return the parsed command without assigning a message first
        if arg_count == 2:
            return parsed_cmd

        message = self.args[1]

        if not isinstance(message, str):
            raise InvalidArgumentError("Invalid message provided, must be of type string!")

        parsed_cmd.message = message

        return parsed_cmd

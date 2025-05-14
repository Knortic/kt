class InvalidArgumentError(Exception):
    pass

class CommandLineArgsParser:
    def __init__(self, *args):
        self.args = list(args)

    def process_args(self):
        if not (self.args[0].isnumeric()):
            raise InvalidArgumentError("Invalid first argument, must be numeric!")

        is_time_negative = int(self.args[0]) < 0
        has_too_many_args = len(self.args) > 2

        if has_too_many_args:
            raise InvalidArgumentError("Arguments exceeded size of 2!")
        elif (is_time_negative):
            raise InvalidArgumentError("Specified time cannot be negative!")
        return self.args

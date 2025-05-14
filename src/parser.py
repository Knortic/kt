class InvalidArgumentError(Exception):
    pass

MAX_ARGS = 2

class CommandLineArgsParser:
    def __init__(self, *args):
        self.args = list(args)

    def process_args(self):
        has_too_many_args = len(self.args) > MAX_ARGS
        if has_too_many_args:
            raise InvalidArgumentError("Arguments exceeded size of 2!")

        duration = self.args[0]

        if not (duration.isnumeric()):
            raise InvalidArgumentError("Invalid first argument, must be numeric!")
        elif (int(duration) < 0):
            raise InvalidArgumentError("Specified duration cannot be negative!")

        description = self.args[1]

        if not isinstance(description, str):
            raise InvalidArgumentError("Invalid second argument, must be of type string!")

        return self.args

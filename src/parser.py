class InvalidArgumentError(Exception):
    pass

class CommandLineArgsParser:
    def __init__(self, *args):
        self.args = list(args)

    def process_args(self):
        if len(self.args) > 2:
            raise InvalidArgumentError("Arguments exceeded size of 2!")
        return self.args

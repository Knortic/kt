from src.parser import CommandLineArgsParser

class Timer:
    def __init__(self, parser, writer):
        self.parser = parser
        self.writer = writer
        self.active = False

    def is_active(self):
        return self.active

    def create(self):
        return True

    def start(self):
        self.active = True
        self.writer.write()

    def stop(self):
        self.active = False


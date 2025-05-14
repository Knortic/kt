from src.parser import CommandLineArgsParser

class Timer:
    def __init__(self, parser):
        self.parser = parser
        self.active = False

    def is_active(self):
        return self.active

    def create(self):
        return True

    def start(self):
        self.active = True


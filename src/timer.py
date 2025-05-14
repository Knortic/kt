from src.parser import CommandLineArgsParser

class Timer:
    def __init__(self, parser):
        self.parser = parser

    def is_active(self):
        return False

    def create(self):
        return True

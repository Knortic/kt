from abc import ABC, abstractmethod
from datetime import datetime

class IWriter(ABC):
    @abstractmethod
    def write(self) -> None:
        pass

class FileWriter(IWriter):
    def __init__(self, timestamp):
        self.timestamp = timestamp

    def write(self):
        pass

class FakeFileWriter(IWriter):
    def __init__(self, timestamp):
        self.timestamp = timestamp
        self.write_amount = 0
        self.returned_filename = ""

    def write(self):
        self.write_amount += 1
        self.returned_filename = self.timestamp.strftime("%Y%m%d_%H%M%S")
 

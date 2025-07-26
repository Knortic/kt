import json

from abc import ABC, abstractmethod

class IReader(ABC):
    @abstractmethod
    def read(self) -> None:
        pass

class FileReader(IReader):
    def __init__(self, path):
        self.path = path
        self.read_content = ""

    def read_with_path(self, path):
        try:
            with open(path, "r") as file:
                self.read_content = file.read()
        except FileNotFoundError:
            print("The file path does not exist.")
        except PermissionError:
            print("You do not have permission to read at this location.")
        except OSError as e:
            print(f"An OS error occurred: {e}")

    def read(self):
        self.read_with_path(self.path)

class FakeFileReader(IReader):
    def __init__(self):
        self.read_amount = 0

    def read(self):
        self.read_amount += 1
 


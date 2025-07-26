from abc import ABC, abstractmethod
from datetime import datetime

class IWriter(ABC):
    @abstractmethod
    def write(self) -> None:
        pass

class FileWriter(IWriter):
    def __init__(self, path):
        self.path = path
        self.write_content = ""

    def write_with_path(self, path):
        if (len(self.write_content) == 0):
            raise RuntimeError("Invalid write content")

        try:
            with open(path, "w") as file:
                file.write(self.write_content)
        except FileNotFoundError:
            print("The file path does not exist.")
        except PermissionError:
            print("You do not have permission to write to this location.")
        except OSError as e:
            print(f"An OS error occurred: {e}")

    def write(self):
        self.write_with_path(self.path)

class FakeFileWriter(IWriter):
    def __init__(self):
        self.write_amount = 0

    def write(self):
        self.write_amount += 1
 

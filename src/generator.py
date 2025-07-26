from abc import ABC, abstractmethod

class IDataGenerator(ABC):
    @abstractmethod
    def generate_data(self) -> None:
        pass

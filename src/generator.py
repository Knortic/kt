from abc import ABC, abstractmethod

class IDataGenerator(ABC):
    @abstractmethod
    def generate_data_from_existing(self) -> None:
        pass

    @abstractmethod
    def generate_data(self) -> None:
        pass

    @abstractmethod
    def fetch_data(self):
        pass

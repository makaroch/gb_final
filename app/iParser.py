from abc import ABC, abstractmethod


class IParser(ABC):
    @abstractmethod
    def get_data(self):
        pass

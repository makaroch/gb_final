from abc import ABC, abstractmethod


class IParser(ABC):
    @abstractmethod
    def get_one_product(self):
        pass

    @abstractmethod
    def get_many_product(self):
        pass

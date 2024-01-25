from abc import ABC, abstractmethod

from app.core.model import ProductCard


class IParser(ABC):
    @abstractmethod
    async def get_one_product(self) -> list[ProductCard]:
        pass

    @abstractmethod
    async def get_many_product(self):
        pass

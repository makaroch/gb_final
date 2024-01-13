from dataclasses import dataclass
from core.eSorting import Sorts


@dataclass
class RequestPars:
    city: str
    search: str
    sorting: Sorts
    min_price: int = 1_00
    max_prise: int = 10_000_00



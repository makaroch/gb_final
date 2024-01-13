from dataclasses import dataclass
from core.eSorting import Sorts
from core.eDeliveryTime import DeliveryTime


@dataclass
class RequestPars:
    """критерии для запроса"""
    city: str = "Москва"
    search: str = " "
    sorting: Sorts = Sorts.popular
    delivery_time: DeliveryTime = DeliveryTime.five_days
    min_price: int = 1_00
    max_prise: int = 10_000_00

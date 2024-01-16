from app.core.eSorting import Sorts
from app.core.eDeliveryTime import DeliveryTime
from pydantic import BaseModel


class RequestPars(BaseModel):
    """критерии для запроса"""
    search: str
    city: str = "Москва"
    sorting: Sorts = Sorts.popular
    delivery_time: DeliveryTime = DeliveryTime.five_days
    min_price: int = 100
    max_prise: int = 1000000
    quantity: int = 10


class ProductCard(BaseModel):
    name: str
    price: float
    rate: float
    feedbacks: int
    date_delivery: str
    link: str
    img: str = None

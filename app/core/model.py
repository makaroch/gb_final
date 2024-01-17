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


class RequestParsMany(RequestPars):
    search: list[str]


class ProductCard(BaseModel):
    name: str = "Product name"
    price: float = 1500
    rate: float = 4.5
    feedbacks: int = 500
    date_delivery: str = "two_days"
    link: str = "https://gas-kvas.com/grafic/uploads/posts/2023-09/1695931386_gas-kvas-com-p-kartinki-s-kotami-18.jpg"
    img: str = "https://gas-kvas.com/grafic/uploads/posts/2023-09/1695931386_gas-kvas-com-p-kartinki-s-kotami-18.jpg"

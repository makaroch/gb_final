from dataclasses import dataclass


@dataclass
class ProductCard:
    name: str
    price: float
    rate: float
    feedbacks: int
    date_delivery: str
    link: str
    img: str = None

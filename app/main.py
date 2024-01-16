import uvicorn
from fastapi import FastAPI

from app.core.eDeliveryTime import DeliveryTime
from app.core.eSorting import Sorts
from app.core.model import ProductCard, RequestPars
from app.wb_pars.WildberriesParser import WildberriesParser

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/wb_product")
def get_wb_product(search: str, city: str = "Москва",
                         sorting: Sorts = Sorts.popular,
                         delivery_time: DeliveryTime = DeliveryTime.five_days,
                         min_price: int = 100,
                         max_prise: int = 1000000,
                         quantity: int = 10) -> list[ProductCard]:
    return WildberriesParser(RequestPars(
        search=search, sorting=sorting, delivery_time=delivery_time,
        min_price=min_price, max_prise=max_prise, quantity=quantity, city=city
    )).get_data()


if __name__ == "__main__":
    # noinspection PyInterpreter
    uvicorn.run(app=app,
                host='127.0.0.1',
                port=80
                )

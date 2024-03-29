from pprint import pprint

import uvicorn
from fastapi import FastAPI

from app.core.eDeliveryTime import DeliveryTime
from app.core.eSorting import Sorts
from app.core.model import ProductCard, RequestPars, RequestParsMany
from app.ozon_pars.OzonParser import OzonParser
from app.wb_pars.WildberriesParser import WildberriesParser

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/get_product")
async def get_product(search: str, city: str = "Москва",
                      sorting: Sorts = Sorts.popular,
                      delivery_time: DeliveryTime = DeliveryTime.five_days,
                      min_price: int = 1,
                      max_prise: int = 10000,
                      quantity: int = 10) -> list[ProductCard] | list:
    wb_res = await WildberriesParser(
        RequestPars(search=search, sorting=sorting, delivery_time=delivery_time,
                    min_price=min_price * 100, max_prise=max_prise * 100, quantity=quantity,
                    city=city.lower())).get_one_product()
    ozon_res = await OzonParser(
        RequestPars(search=search, sorting=sorting, delivery_time=delivery_time,
                    min_price=min_price * 100, max_prise=max_prise * 100, quantity=quantity,
                    city=city.lower())).get_one_product()
    common_res = wb_res + ozon_res

    if sorting == Sorts.popular:
        common_res = sorted(common_res, key=lambda x: x.feedbacks, reverse=True)
    elif sorting == Sorts.rate:
        common_res = sorted(common_res, key=lambda x: x.rate, reverse=True)
    elif sorting == Sorts.price_up:
        common_res = sorted(common_res, key=lambda x: x.price)
    elif sorting == Sorts.price_down:
        common_res = sorted(common_res, key=lambda x: x.price, reverse=True)

    return common_res

@app.get("/wb_product")
async def get_wb_product(search: str, city: str = "Москва",
                         sorting: Sorts = Sorts.popular,
                         delivery_time: DeliveryTime = DeliveryTime.five_days,
                         min_price: int = 1,
                         max_prise: int = 10000,
                         quantity: int = 10) -> list[ProductCard] | list:
    return await WildberriesParser(
        RequestPars(search=search, sorting=sorting, delivery_time=delivery_time,
                    min_price=min_price * 100, max_prise=max_prise * 100, quantity=quantity,
                    city=city.lower())).get_one_product()


@app.post("/wb_products")
async def get_wb_products(request: RequestParsMany) -> list[list[ProductCard]]:
    return await WildberriesParser(request).get_many_product()


@app.get("/ozon_product")
async def get_ozon_product(search: str, city: str = "Москва",
                           sorting: Sorts = Sorts.popular,
                           delivery_time: DeliveryTime = DeliveryTime.five_days,
                           min_price: int = 1,
                           max_prise: int = 10000,
                           quantity: int = 10) -> list[ProductCard] | list:
    return await OzonParser(
        RequestPars(search=search, sorting=sorting, delivery_time=delivery_time,
                    min_price=min_price * 100, max_prise=max_prise * 100, quantity=quantity,
                    city=city.lower())).get_one_product()


@app.post("/ozon_products")
async def get_wb_products(request: RequestParsMany) -> list[list[ProductCard]]:
    return [[ProductCard()], [ProductCard()]]


if __name__ == "__main__":
    uvicorn.run(app=app,
                host='127.0.0.1',
                port=80
                )

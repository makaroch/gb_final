from typing import List

import requests

from app.iParser import IParser
from app.core.model import RequestPars, ProductCard
from app.core.PointIssueInfo import PointIssueInfo
from app.wb_pars.GetDestPoint import GetDestPoint


class WildberriesParser(IParser):
    def __init__(self, search_query):
        self.__search_query: RequestPars = search_query
        self.__geo_loc = GetDestPoint()

    def __pars(self) -> dict:
        self.__point_issue_info: PointIssueInfo = self.__geo_loc.get_dest(self.__search_query.city.lower())
        print(self.__point_issue_info)
        min_prace: int = self.__search_query.min_price
        max_prace: int = self.__search_query.max_prise
        query: str = self.__search_query.search
        sort: str = self.__search_query.sorting.value
        dlvr = self.__search_query.delivery_time.value

        url = (f"https://search.wb.ru/exactmatch/ru/common/v4/search?TestGroup=control&TestID=391&appType=1"
               f"&curr=rub&dest={self.__point_issue_info.dest}&priceU={min_prace};{max_prace}&fdlvr={dlvr}&page=1"
               f"&query={query}&resultset=catalog&sort={sort}&spp=29&suppressSpellcheck=false")

        return requests.get(url).json()

    def __create_img_link(self, _id: int) -> str:
        _id = int(_id)
        _short_id = _id // 100000
        if 0 <= _short_id <= 143:
            basket = '01'
        elif 144 <= _short_id <= 287:
            basket = '02'
        elif 288 <= _short_id <= 431:
            basket = '03'
        elif 432 <= _short_id <= 719:
            basket = '04'
        elif 720 <= _short_id <= 1007:
            basket = '05'
        elif 1008 <= _short_id <= 1061:
            basket = '06'
        elif 1062 <= _short_id <= 1115:
            basket = '07'
        elif 1116 <= _short_id <= 1169:
            basket = '08'
        elif 1170 <= _short_id <= 1313:
            basket = '09'
        elif 1314 <= _short_id <= 1601:
            basket = '10'
        elif 1602 <= _short_id <= 1655:
            basket = '11'
        elif 1656 <= _short_id <= 1919:
            basket = '12'
        else:
            basket = '13'
        return f"https://basket-{basket}.wbbasket.ru/vol{_short_id}/part{_id // 1000}/{_id}/images/big/1.webp"

    def __pars_response(self, raw_response: dict) -> List[ProductCard]:
        lst = []
        products: list = raw_response.get("data").get("products")

        for i in range(self.__search_query.quantity):
            product: dict = products[i]
            prod_card = ProductCard(
                name=product.get("name"),
                price=int(product.get("salePriceU")) // 100,
                rate=product.get("supplierRating"),
                feedbacks=product.get("feedbacks"),
                date_delivery=self.__search_query.delivery_time.name,
                link=f"https://www.wildberries.ru/catalog/{product.get('id')}/detail.aspx",
                img=self.__create_img_link(product.get('id'))
            )
            lst.append(prod_card)

        return lst

    def get_data(self):
        raw_response: dict = (self.__pars())
        if len(raw_response) == 0 or len(raw_response.get("data").get("products")) == 0:
            return {}
        return self.__pars_response(raw_response)



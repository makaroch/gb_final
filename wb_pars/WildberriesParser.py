import requests
import pprint

from core.eDeliveryTime import DeliveryTime
from core.eSorting import Sorts
from iParser import IParser
from core.RequestPars import RequestPars
from core.PointIssueInfo import PointIssueInfo
from wb_pars.GetDestPoint import GetDestPoint


class WildberriesParser(IParser):
    def __init__(self, search_query):
        self.__search_query: RequestPars = search_query

    def __pars(self) -> dict:
        self.__point_issue_info: PointIssueInfo = GetDestPoint(self.__search_query.city).get_dest()
        min_prace: int = self.__search_query.min_price
        max_prace: int = self.__search_query.max_prise
        query: str = self.__search_query.search
        sort: str = self.__search_query.sorting.value
        dlvr = self.__search_query.delivery_time.value

        url = (f"https://search.wb.ru/exactmatch/ru/common/v4/search?TestGroup=control&TestID=391&appType=1"
               f"&curr=rub&dest={self.__point_issue_info.dest}&priceU={min_prace};{max_prace}&fdlvr={dlvr}&page=1"
               f"&query={query}&resultset=catalog&sort={sort}&spp=29&suppressSpellcheck=false")

        response = requests.get(url)
        print(response.json())

    def get_data(self):
        self.__pars()


if __name__ == "__main__":
    WildberriesParser(RequestPars(city="Москва", search="акпк")).get_data()

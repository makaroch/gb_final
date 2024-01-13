
import requests

from iParser import IParser
from core.RequestPars import RequestPars
from typing import NamedTuple
from geopy.geocoders import Nominatim


class Coordinates(NamedTuple):
    latitude: float
    longitude: float


class WildberriesParser(IParser):
    def __init__(self, search_query):
        self.__search_query: RequestPars = search_query

    def __get_latitude_longitude(self) -> Coordinates:
        """найти координаты города"""
        nominatim = Nominatim(user_agent="user")

        location = nominatim.geocode(f"{self.__search_query.city}, Russia")
        if location is None:
            return Coordinates(latitude=0, longitude=0)

        return Coordinates(latitude=location[1][0], longitude=location[1][1])

    def __get_issue_point_number(self) -> int:
        geo_coord = self.__get_latitude_longitude()

        url = (f"https://user-geo-data.wildberries.ru/get-geo-info?currency=RUB&latitude={geo_coord.latitude}"
               f"&longitude={geo_coord.longitude}&locale=ru&address=%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0&dt=0")
        print(requests.get(url).json())
        return 0

    def __pars(self) -> dict[str:str]:
        issue_point_number = self.__get_issue_point_number()
        min_prace = self.__search_query.min_price
        max_prace = self.__search_query.max_prise
        query = self.__search_query.search
        sort = self.__search_query.sorting.value
        url = (f"https://search.wb.ru/exactmatch/ru/common/v4/search?TestGroup=control&TestID=391&appType=1"
               f"&curr=rub&dest={issue_point_number}&priceU={min_prace};{max_prace}&fdlvr=81&page=1&query={query}"
               f"&resultset=catalog&sort={sort}&spp=29&suppressSpellcheck=false")

        # response = requests.get(url,cookies=)




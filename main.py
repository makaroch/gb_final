import pprint

from core.RequestPars import RequestPars
from core.eSorting import Sorts
from core.eDeliveryTime import DeliveryTime
from wb_pars.WildberriesParser import WildberriesParser

if __name__ == "__main__":
    pprint.pprint(WildberriesParser(RequestPars(city="сочи",
                                                search="лампа",
                                                sorting=Sorts.rate,
                                                delivery_time=DeliveryTime.two_days,
                                                min_price=50000,
                                                max_prise=100000,
                                                quantity=20
                                                )).get_data())
    pprint.pprint(WildberriesParser(RequestPars(city="сочи",
                                                search="werghj",
                                                sorting=Sorts.rate,
                                                delivery_time=DeliveryTime.two_days,
                                                min_price=50000,
                                                max_prise=100000,
                                                quantity=20
                                                )).get_data())
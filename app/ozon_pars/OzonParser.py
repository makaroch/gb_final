from app.core.model import RequestPars, ProductCard
from app.iParser import IParser
from random import randint

class OzonParser(IParser):
    def __init__(self, request_criteria: RequestPars):
        self.__request_criteria = request_criteria
        pass

    # def __pars(self):
    #     with sync_playwright() as playwright:
    #         browser = playwright.chromium.launch(headless=False)
    #         self.context = browser.new_context()
    #         self.page = self.context.new_page()
    #         self.page.goto("https://www.ozon.ru/")
    #         self.page.get_by_placeholder("Искать на Ozon").type(text=self.__keyword, delay=0.3)
    #         self.page.query_selector("button[type='submit']").click()
    #         time.sleep(5)
    #         # self.__get_links()

    async def get_one_product(self) -> list[ProductCard]:
        lst = []
        date_delivery_rnd = ["two_days", "three_days", "five_days"]
        min_index_delivery_rnd = 0
        max_index_delivery_rnd = 0

        if self.__request_criteria.delivery_time == "76":
            max_index_delivery_rnd = 1
        elif self.__request_criteria.delivery_time == "124":
            max_index_delivery_rnd = 2

        for i in range(self.__request_criteria.quantity):
            prod_card = ProductCard(
                name=self.__request_criteria.search,
                price=randint(self.__request_criteria.min_price, self.__request_criteria.max_prise) / 100,
                rate=randint(1,5),
                feedbacks=randint(10, 500),
                date_delivery=date_delivery_rnd[randint(min_index_delivery_rnd, max_index_delivery_rnd)],
                link=f"https://www.ozon.ru/",
                img="https://catherineasquithgallery.com/uploads/posts/2021-02/1612275654_86-p-kot-na-fioletovom-fone-104.jpg"
            )
            lst.append(prod_card)
        return lst

    async def get_many_product(self):
        pass

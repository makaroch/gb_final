from time import sleep
from playwright.sync_api import sync_playwright

from core.PointIssueInfo import PointIssueInfo


class GetDestPoint:
    def __init__(self, city_name):
        self.__city_name: str = city_name
        self.__url: str = "https://www.wildberries.ru/"
        self.__raw_dest: dict = None

    def __get_log(self, msg):
        result = []
        for arg in msg.args:
            result.append(dict(arg.json_value()))
        self.__raw_dest = result[0]

    def __pars_log(self) -> PointIssueInfo:
        return PointIssueInfo(latitude=self.__raw_dest["geometry"]["coordinates"][0],
                              longitude=self.__raw_dest["geometry"]["coordinates"][1],
                              dest=self.__raw_dest["properties"]["pooData"]["dest"])

    def get_dest(self) -> PointIssueInfo:
        """получить по названию города dest(нужен для определения сроков доставки)"""
        if self.__city_name.lower() == "москва":
            return PointIssueInfo(
                latitude=55.753493,
                longitude=37.596546,
                dest="-1257786",
            )

        with sync_playwright() as playwright:
            browser = playwright.chromium.launch()
            context = browser.new_context()
            page = context.new_page()
            page.goto(self.__url)
            sleep(3)

            page.click(".simple-menu__link")  # открытие карты для выбора точки
            page.wait_for_selector(".ymaps-2-1-79-searchbox-input__input")
            page.query_selector(".ymaps-2-1-79-searchbox-input__input").type(text=self.__city_name,
                                                                             delay=0.3)  # ввод гороа
            # выераем первый в списке
            page.keyboard.press("ArrowDown")
            page.keyboard.press("Enter")
            # еше раз выберам город
            page.wait_for_selector(".ymaps-2-1-79-islets__first")
            page.click(".ymaps-2-1-79-islets__first")
            # ждем когда закрузяться ПВЗ кликакаем на первый в списке
            page.wait_for_selector(".address-item__wrap")
            page.on("console", self.__get_log)
            page.click(".address-item__wrap")

            self.__pars_log()
        return self.__pars_log()

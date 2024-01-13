from time import sleep
from playwright.sync_api import sync_playwright


class GetDestPoint:
    def __init__(self, city_name):
        self.__city_name = city_name
        self.__url = "https://www.wildberries.ru/"
        self.__raw_dest = None
        self.__dest = None

    def __get_log(self, msg):
        result = []
        for arg in msg.args:
            result.append(dict(arg.json_value()))
        self.__raw_dest = result[0]

    def __pars_log(self):
        self.__dest = self.__raw_dest["properties"]["pooData"]["dest"]
        pass

    def get_dest(self) -> str:
        """получить по названию города dest(нужен для определения сроков доставки)"""
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch()
            context = browser.new_context()
            page = context.new_page()
            page.goto(self.__url)
            sleep(3)

            page.click(".simple-menu__link") # открытие карты для выбора точки
            page.wait_for_selector(".ymaps-2-1-79-searchbox-input__input")
            page.query_selector(".ymaps-2-1-79-searchbox-input__input").type(text=self.__city_name, delay=0.3) # ввод гороа
            # выераем первый в списке
            page.keyboard.press("ArrowDown")
            page.keyboard.press("Enter")
            # еше раз выберам город
            page.wait_for_selector(".ymaps-2-1-79-islets__first")
            page.click(".ymaps-2-1-79-islets__first")
            # ждем когда закрузяться ПВТ кликакаем на первый в списке
            page.wait_for_selector(".address-item__wrap")
            page.on("console", self.__get_log)
            page.click(".address-item__wrap")

            self.__pars_log()
        return self.__dest

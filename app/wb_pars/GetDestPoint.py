import asyncio

from playwright.async_api import async_playwright, Playwright

from app.core.PointIssueInfo import PointIssueInfo


def caching(funk):
    __cache: dict[str, PointIssueInfo] = {}

    async def inner(*args, **kwargs):
        if args[1] in __cache:
            return __cache.get(args[1])
        __cache[args[1]] = await funk(*args, **kwargs)
        return __cache.get(args[1])

    return inner


class GetDestPoint:
    def __init__(self, ):
        self.__url: str = "https://www.wildberries.ru/"
        self.__raw_dest: dict = {}

    async def __get_log(self, msg):
        result = []
        for arg in msg.args:
            result.append(await arg.json_value())
        self.__raw_dest = result[0]
    async def __pars_log(self) -> PointIssueInfo:
        return PointIssueInfo(latitude=self.__raw_dest["geometry"]["coordinates"][0],
                              longitude=self.__raw_dest["geometry"]["coordinates"][1],
                              dest=self.__raw_dest["properties"]["pooData"]["dest"])

    @caching
    async def get_dest(self, city_name: str) -> PointIssueInfo:
        """получить по названию города dest(нужен для определения сроков доставки)"""
        print(city_name)
        if city_name == "москва":
            return PointIssueInfo(
                latitude=55.753493,
                longitude=37.596546,
                dest="-1257786",
            )

        async with async_playwright() as playwright:
            browser = await playwright.chromium.launch()
            context = await browser.new_context()
            page = await context.new_page()
            await page.goto(self.__url)
            await asyncio.sleep(2)

            await page.click(".simple-menu__link")  # открытие карты для выбора точки
            await page.wait_for_selector(".ymaps-2-1-79-searchbox-input__input")
            search_element = await page.query_selector(".ymaps-2-1-79-searchbox-input__input")
            await search_element.type(text=city_name, delay=0.3)  # ввод гороа
            # выераем первый в списке
            await page.keyboard.press("ArrowDown")
            await page.keyboard.press("Enter")
            # еше раз выберам город
            await page.wait_for_selector(".ymaps-2-1-79-islets__first")
            await page.click(".ymaps-2-1-79-islets__first")
            # await asyncio.sleep(1)

            # ждем когда закрузяться ПВЗ кликакаем на первый в списке
            await page.wait_for_selector(".address-item__wrap")
            page.on("console", self.__get_log)
            await page.click(".address-item__wrap")
            await browser.close()

        return await self.__pars_log()

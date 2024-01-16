import time
from playwright.sync_api import sync_playwright
from app.core.model import RequestPars


class OzonParser:
    def __init__(self, request_criteria: RequestPars):
        self.__keyword = request_criteria.search
        pass

    def pars(self):
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=False)
            self.context = browser.new_context()
            self.page = self.context.new_page()
            self.page.goto("https://www.ozon.ru/")
            self.page.get_by_placeholder("Искать на Ozon").type(text=self.__keyword, delay=0.3)
            self.page.query_selector("button[type='submit']").click()
            time.sleep(5)
            # self.__get_links()


OzonParser(RequestPars(search="мышь")).pars()

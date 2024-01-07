from playwright.sync_api import sync_playwright, expect
from bs4 import BeautifulSoup
from typing import Union, Optional
import time
import re


class TheatreParse:
    def __init__(self):
        self.URL = 'https://teatr15.ru/'
        self.page = None
        self.context = None

    def __get_iframe_id(self, html: str) -> Optional[str]:
        soup = BeautifulSoup(html, 'lxml')
        iframes = soup.find_all('iframe')

        if len(iframes):
            for iframe in iframes:
                if "https://radario.ru/customer/afisha" in iframe.get('src'):
                    return iframe.get('id')
        return None

    def parse(self):
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=False)
            self.context = browser.new_context()
            self.page = self.context.new_page()
            self.page.goto(self.URL)

            self.page.get_by_role("link", name="Купить билет").click()
            self.page.wait_for_timeout(5_000)
            self.page.mouse.wheel(0, 150_000)

            is_exists_btn_load_more = self.page.frame_locator("#RadarioIframe2").get_by_role(
                "button",
                name="Загрузить еще").is_visible()

            task_iframe_id = self.__get_iframe_id(self.page.content())

            while is_exists_btn_load_more:
                self.page.frame_locator(f"#{task_iframe_id}").get_by_role("button", name="Загрузить еще").click()
                self.page.wait_for_timeout(5_000)
                self.page.mouse.wheel(0, 150_000)
                is_exists_btn_load_more = self.page.frame_locator("#RadarioIframe2").get_by_role(
                    "button",
                    name="Загрузить еще").is_visible()

            self.page.wait_for_timeout(7_000)


if __name__ == '__main__':
    TheatreParse().parse()

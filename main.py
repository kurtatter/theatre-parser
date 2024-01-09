from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from apscheduler.schedulers.blocking import BlockingScheduler

from typing import Union, Optional
import re

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Ticket

engine = create_engine("sqlite:///data.db")
Session = sessionmaker(engine)


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

    def __format_text(self, text: str) -> str:
        return re.sub("\s{2,}", " ",
                      " ".join(text.strip().split("\n"))
                      )

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
            with Session(bind=engine) as session:

                for loc in self.page.frame_locator("#RadarioIframe2").locator(".card-wrapper").all():
                    card_head = self.__format_text(
                        loc.locator(".card-head").text_content()
                    )
                    tickets_price = self.__format_text(
                        loc.locator(".card-footer").get_by_role("button").text_content()
                    )
                    tickets_count = self.__format_text(
                        loc.locator(".card-footer").locator(".card__tickets").text_content()
                    )
                    cover_date = self.__format_text(
                        loc.locator(".card-cover__date").text_content()
                    )

                    print(card_head)
                    print(tickets_price)
                    print(tickets_count)
                    print(cover_date)
                    print()
                    session.add(
                        Ticket(
                            card_head,
                            tickets_price,
                            tickets_count,
                            cover_date
                        )
                    )
                session.commit()
            self.page.wait_for_timeout(7_000)


if __name__ == '__main__':
    TheatreParse().parse()
    # def some_job():
    #     TheatreParse().parse()
    #
    #
    # scheduler = BlockingScheduler()
    # scheduler.add_job(some_job, 'interval', hours=1)
    # scheduler.start()

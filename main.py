from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from apscheduler.schedulers.blocking import BlockingScheduler

from typing import Optional, List, Dict
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

    def __save_tickets(self, tickets: List[Dict]):
        with Session(bind=engine) as session:
            for ticket in tickets:
                session.add(
                    Ticket(
                        ticket.get("title"),
                        ticket.get("price"),
                        ticket.get("count"),
                        ticket.get("date"),
                        True
                    )
                )

            session.commit()

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

            tickets = list()

            for loc in self.page.frame_locator("#RadarioIframe2").locator(".card-wrapper").all():
                card_head = self.__format_text(
                    loc.locator(".card-head").text_content()
                )
                tickets_price = self.__format_text(
                    loc.locator(".card-footer").get_by_role("button").text_content()
                )

                ticket_price_disabled = not bool(loc.locator(".card-footer").
                                                 get_by_role("button").get_attribute("disabled"))

                tickets_count = self.__format_text(
                    loc.locator(".card-footer").locator(".card__tickets").text_content()
                )
                cover_date = self.__format_text(
                    loc.locator(".card-cover__date").text_content()
                )

                tickets.append({
                    "title": card_head,
                    "price": tickets_price,
                    "price_is_active": ticket_price_disabled,
                    "count": tickets_count,
                    "date": cover_date
                })

            self.__save_tickets(tickets)
            print(tickets)

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

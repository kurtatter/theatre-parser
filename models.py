from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime

from datetime import datetime

Base = declarative_base()


class User(Base):
    __tablename__ = "User"

    id = Column(Integer, primary_key=True)
    name = Column(String(264))


class Ticket(Base):
    __tablename__ = "Ticket"

    id = Column(Integer, primary_key=True)
    create_datetime = Column(DateTime, default=datetime.now, name="createDatetime")

    title = Column(String(500))
    price = Column(String(128))
    count = Column(String(128))
    date_time = Column(DateTime, name="dateTime")

    def __str__(self):
        return self.title

    def __repr__(self):
        return self.title

    def __get_month_number_from_name(self, month_name: str) -> int:
        months = (
            "январ",
            "феврал",
            "март",
            "апрел",
            "мая",
            "июн",
            "июл",
            "август",
            "сентябр",
            "октябр",
            "ноябр",
            "декабр",
        )

        for n, m in enumerate(months):
            if m in month_name:
                return n + 1

    def __parse_date_time(self, date_time: str) -> datetime:
        date_time_values = date_time.split()
        return datetime(
            datetime.now().year,
            self.__get_month_number_from_name(date_time_values[1]),
            int(date_time_values[0]),
            int(date_time_values[2].split(':')[0]),
            int(date_time_values[2].split(':')[1])
        )

    def __init__(self, title: str, price: str, count: str, date_time: str) -> None:
        self.title = title
        self.price = price
        self.count = count
        self.date_time = self.__parse_date_time(date_time)

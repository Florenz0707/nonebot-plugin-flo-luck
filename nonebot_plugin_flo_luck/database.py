import datetime
import sqlite3
from enum import Enum
from nonebot.log import logger
from pathlib import Path

data_dir = Path("data/flo_luck").absolute()
data_dir.mkdir(parents=True, exist_ok=True)


class SelectType(Enum):
    BY_WEEK = 0
    BY_MONTH = 1
    BY_YEAR = 2
    BY_NONE = 3


def today() -> str:
    return datetime.date.today().strftime("%y%m%d")


class DataBase:
    def __init__(self):
        self.luck_db = sqlite3.connect("data/flo_luck/database.db")
        self.cursor = self.luck_db.cursor()
        try:
            create_table = """
            CREATE TABLE IF NOT EXISTS luck_data
            (user_id text,
            date     text,
            val      int);
            """
            self.cursor.execute(create_table)
        except sqlite3.Error as error:
            logger.error(f"create luck_data db failed: {str(error)}")

    def __del__(self):
        self.cursor.close()
        self.luck_db.close()

    def insert(self, user_id: str, val: int, date: str = today()) -> None:
        self.cursor.execute(
            "insert into luck_data (user_id, date, val) values (?, ?, ?)",
            (user_id, date, val))
        self.luck_db.commit()

    def remove(self, user_id: str, date: str) -> None:
        self.cursor.execute(
            "delete from luck_data where user_id = ? and date = ?",
            (user_id, date)
        )
        self.luck_db.commit()

    def select_by_user_date(self, user_id: str, date: str = today()) -> int:
        self.cursor.execute(
            "select val from luck_data where user_id = ? and date = ?",
            (user_id, date)
        )
        result = self.cursor.fetchone()
        if result is None:
            return -1
        return result[0]

    def select_by_user(self, user_id: str) -> list[str, int]:
        self.cursor.execute(
            "select date, val from luck_data where user_id = ?",
            (user_id,)
        )
        result = self.cursor.fetchall()
        return result

    def select_by_range(self, user_id: str, select_mode: SelectType) -> list[int]:
        raw_data = self.select_by_user(user_id)
        result = list()
        today_string = datetime.datetime.strptime(today(), "%y%m%d")
        for date, val in raw_data:
            res_string = datetime.datetime.strptime(date, "%y%m%d")
            if select_mode == SelectType.BY_WEEK:
                flag = (today_string.isocalendar()[1] == res_string.isocalendar()[1]
                        and today_string.year == res_string.year)
            elif select_mode == SelectType.BY_MONTH:
                flag = (today_string.year == res_string.year
                        and today_string.month == res_string.month)
            elif select_mode == SelectType.BY_YEAR:
                flag = (today_string.year == res_string.year)
            else:
                flag = True
            if flag:
                result.append(val)

        return result

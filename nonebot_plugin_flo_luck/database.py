import sqlite3
from .helper_functions import *
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


class LuckDataBase:
    def __init__(self):
        self.luck_db = sqlite3.connect("data/flo_luck/flo_luck.db")
        self.cursor = self.luck_db.cursor()
        self.ave_id = "average"  # 特殊user_id，用于记录每日平均值
        try:
            create_table = """
            create table if not exists luck_data
            (user_id text,
            date     text,
            val      int);
            """
            self.cursor.execute(create_table)
            self.luck_db.commit()
        except sqlite3.Error as error:
            logger.error(f"create table luck_data in flo_luck.db failed: {str(error)}")

    def __del__(self):
        self.cursor.close()
        self.luck_db.close()

    def insert(self, user_id: str, val: int, date: str = today()) -> None:
        self.cursor.execute(
            "insert into luck_data (user_id, date, val) values (?, ?, ?)",
            (user_id, date, val))
        self.luck_db.commit()
        self.update_average()

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

    def select_by_date(self, date: str = today()) -> list[tuple[str, int]]:
        self.cursor.execute(
            "select user_id, val from luck_data where date = ?",
            (date,)
        )
        return self.cursor.fetchall()

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

    def update_average(self) -> None:
        if self.select_by_user_date(self.ave_id) == -1:
            # 当日还未创建平均值记录
            self.insert(self.ave_id, 0)
        values = [pair[1] for pair in self.select_by_date()]
        self.cursor.execute(
            "update luck_data set val = ? where user_id = ? and date = ?",
            (int(get_average(values)[1]), self.ave_id, today())
        )
        self.luck_db.commit()

    def select_average(self, date: str = today()) -> int:
        return self.select_by_user_date(self.ave_id, date)


class SpecialDataBase:
    def __init__(self):
        self.luck_db = sqlite3.connect("data/flo_luck/flo_luck.db")
        self.cursor = self.luck_db.cursor()
        try:
            create_table = """
                    create table if not exists special_data
                    (user_id text,
                    greeting text,
                    bottom   int,
                    top      int,
                    primary key(user_id)
                    )
                    """
            self.cursor.execute(create_table)
            self.luck_db.commit()
        except sqlite3.Error as error:
            logger.error(f"create table special_data in luck.db failed: {str(error)}")

    def __del__(self):
        self.cursor.close()
        self.luck_db.close()

    def insert(self, user_id: str, greeting: str = "", bottom: int = 0, top: int = 100) -> bool:
        try:
            self.cursor.execute(
                "insert into special_data (user_id, greeting, bottom, top) values (?, ?, ?, ?)",
                (user_id, greeting, bottom, top)
            )
        except sqlite3.IntegrityError as error:
            logger.error(f"Error occurs when inserted into where user_id = {user_id}. Info: {str(error)}")
            return False
        else:
            self.luck_db.commit()
            return True

    def remove(self, user_id: str) -> None:
        self.cursor.execute(
            "delete from special_data where user_id = ?",
            (user_id,)
        )
        self.luck_db.commit()

    def select_by_user(self, user_id: str) -> list:
        self.cursor.execute(
            "select greeting, bottom, top from special_data where user_id = ?",
            (user_id,)
        )
        return self.cursor.fetchone()

    def select_all(self) -> list:
        self.cursor.execute(
            "select user_id, greeting, bottom, top from special_data"
        )
        return self.cursor.fetchall()

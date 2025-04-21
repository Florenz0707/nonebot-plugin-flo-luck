import sqlite3
from .helper_functions import *
from enum import Enum
from nonebot.log import logger
from nonebot import require
from pathlib import Path

require("nonebot_plugin_localstore")
import nonebot_plugin_localstore as localstore

plugin_data_dir: Path = localstore.get_plugin_data_dir()
plugin_data_file: Path = localstore.get_plugin_data_file("flo_luck.db")

"""
Define database including
LuckDataBase storing luck_val using user_id, date & val,
SpecialDataBase storing special list using user_id, greeting, bottom & top.
"""


class SelectType(Enum):
    BY_WEEK = 0
    BY_MONTH = 1
    BY_YEAR = 2
    BY_NONE = 3


class LuckDataBase:
    def __init__(self):
        self.luck_db = sqlite3.connect(plugin_data_file)
        self.cursor = self.luck_db.cursor()
        self.ave_id = "average"  # special user_id for today average
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

    def insert(self, user_id: str, val: int, date: str) -> None:
        self.cursor.execute(
            "insert into luck_data (user_id, date, val) values (?, ?, ?)",
            (user_id, date, val))
        self.luck_db.commit()
        # After insert, update average to avoid frequent access
        self.update_average()

    def remove(self, user_id: str, date: str) -> None:
        # Not use in actually running, reserved for debug
        self.cursor.execute(
            "delete from luck_data where user_id = ? and date = ?",
            (user_id, date)
        )
        self.luck_db.commit()

    def select_by_user_date(self, user_id: str, date: str) -> int:
        # select val via user_id and date, most possibly only one record
        # if not exist, return -1
        self.cursor.execute(
            "select val from luck_data where user_id = ? and date = ?",
            (user_id, date)
        )
        result = self.cursor.fetchone()
        if result is None:
            return -1
        return result[0]

    def select_by_user(self, user_id: str) -> list[tuple[str, int]]:
        # select (date, val) via user_id
        self.cursor.execute(
            "select date, val from luck_data where user_id = ?",
            (user_id,)
        )
        result = self.cursor.fetchall()
        return result

    def select_by_date(self, date: str) -> list[tuple[str, int]]:
        # select (user_id, val) via date
        self.cursor.execute(
            "select user_id, val from luck_data where date = ? and user_id != ?",
            (date, self.ave_id)
        )
        return self.cursor.fetchall()

    def select_by_range(self, user_id: str, select_mode: SelectType) -> list[int]:
        # select a specific time range via user_id
        raw_data = self.select_by_user(user_id)
        if select_mode == SelectType.BY_NONE:
            return [val for date, val in raw_data]
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
                flag = False

            if flag:
                result.append(val)

        return result

    def update_average(self) -> None:
        # should not be called by instance, but relatively by insert
        if self.select_by_user_date(self.ave_id, today()) == -1:
            # no average record for today, insert a record first
            self.cursor.execute(
                "insert into luck_data (user_id, date, val) values (?, ?, ?)",
                (self.ave_id, today(), 0)
            )
            # to avoid calling update again, don't use insert
            self.luck_db.commit()

        values = [val for user_id, val in self.select_by_date(today())]
        self.cursor.execute(
            "update luck_data set val = ? where user_id = ? and date = ?",
            (int(get_average(values)[1]), self.ave_id, today())
        )
        self.luck_db.commit()

    def select_average(self, date: str) -> int:
        return self.select_by_user_date(self.ave_id, date)


class SpecialDataBase:
    def __init__(self):
        self.luck_db = sqlite3.connect(plugin_data_file)
        self.cursor = self.luck_db.cursor()
        try:
            create_table = """
                    create table if not exists special_data(
                        user_id     text,
                        greeting    text,
                        bottom      int,
                        top         int,
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
            self.luck_db.commit()
        except sqlite3.Error as error:
            logger.error(f"Error occurs when insert into special_data where user_id = {user_id}. Info: {str(error)}")
            return False
        else:
            return True

    def update(self, user_id: str, greeting: str = "", bottom: int = 0, top: int = 100) -> bool:
        try:
            self.cursor.execute(
                "update special_data set greeting = ?, bottom = ?, top = ? where user_id = ?",
                (greeting, bottom, top, user_id)
            )
            self.luck_db.commit()
        except sqlite3.Error as error:
            logger.error(f"Error occurs when update special_data where user_id = {user_id}. Info: {str(error)}")
            return False
        else:
            return True

    def remove(self, user_id: str) -> bool:
        try:
            self.cursor.execute(
                "delete from special_data where user_id = ?",
                (user_id,)
            )
            self.luck_db.commit()
        except sqlite3.Error as error:
            logger.error(f"Error occurs when delete from special_data where user_id = {user_id}. Info: {str(error)}")
            return False
        else:
            return True

    def select_by_user(self, user_id: str) -> list:
        self.cursor.execute(
            "select user_id, greeting, bottom, top from special_data where user_id = ?",
            (user_id,)
        )
        return self.cursor.fetchone()

    def select_all(self) -> list:
        self.cursor.execute(
            "select user_id, greeting, bottom, top from special_data"
        )
        return self.cursor.fetchall()

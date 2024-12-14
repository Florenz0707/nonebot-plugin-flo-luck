from datetime import date
from nonebot.log import logger
import sqlite3


class UserConn:
    # (val: int, short_info: str, (long_info_1: str, long_info_2, ...))
    luck_info = (
        (0, "大凶", ("可能有人一直盯着你......", "要不今天咱还是别出门了......"))
    )

    def __init__(self):
        self.luck_data = sqlite3.connect(r"./database.db")
        self.cursor = self.luck_data.cursor()
        try:
            create_table = """
            CREATE TABLE IF NOT EXISTS luck_data
            (UserId int,
            Date text
            Val);
            """
            self.cursor.execute(create_table)
        except sqlite3.Error as error:
            logger.error(f"create luck_data db failed: {str(error)}")
        else:
            logger.log(message="create luck_data db succeeded")
        finally:
            pass

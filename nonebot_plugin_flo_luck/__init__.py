# ------------------------ import ------------------------
# import packages from python
from pathlib import Path
import random
from .database import *
from .config import Config

# import packages from nonebot or other plugins
from nonebot import (
    get_plugin_config,
    load_plugins,
    require
)

from nonebot.plugin import PluginMetadata

require("nonebot_plugin_alconna")
from nonebot_plugin_alconna import *

require("nonebot_plugin_uninfo")
from nonebot_plugin_uninfo import Uninfo

# ------------------------ import ------------------------

__plugin_meta__ = PluginMetadata(
    name="nonebot-plugin-flo-luck",
    description="",
    usage="",
    config=Config,
)

config = get_plugin_config(Config)

sub_plugins = load_plugins(
    str(Path(__file__).parent.joinpath("plugins").resolve())
)

db_conn = DataBase()

# luck value tips
# format: (val: int, short_info: str, (long_info_1: str, long_info_2, ...))
luck_info = (
    (0, "最凶",
     ("要不今天咱们就在床上躲一会吧...害怕...", "保佑。祝你平安。")),
    (1, "大凶",
     ("可能有人一直盯着你......", "要不今天咱还是别出门了......")),
    (10, "凶",
     ("啊这...昨天是不是做了什么不好的事？", "啊哈哈...或许需要多加小心呢。")),
    (20, "末吉",
     ("呜呜，今天运气似乎不太好...", "勉强能算是个吉签吧。")),
    (30, "末小吉",
     ("唔...今天运气有点差哦。", "今天喝水的时候务必慢一点。")),
    (40, "小吉",
     ("还行吧，稍差一点点呢。", "差不多是阴天的水平吧，不用特别担心哦。")),
    (50, "半吉",
     ("看样子是普通的一天呢。一切如常......", "加油哦！今天需要靠自己奋斗！")),
    (60, "吉",
     ("欸嘿...今天运气还不错哦？喜欢的博主或许会更新！", "欸嘿...今天运气还不错哦？要不去抽卡？")),
    (70, "大吉",
     ("好耶！运气非常不错呢！今天是非常愉快的一天 ⌯>ᴗo⌯ .ᐟ.ᐟ", "好耶！大概是不经意间看见彩虹的程度吧？")),
    (80, "祥吉",
     ("哇哦！特别好运哦！无论是喜欢的事还是不喜欢的事都能全部解决！", "哇哦！特别好运哦！今天可以见到心心念念的人哦！")),
    (90, "佳吉",
     ("૮₍ˊᗜˋ₎ა 不用多说，怎么度过今天都会顺意的！", "૮₍ˊᗜˋ₎ა  会发生什么好事呢？真是期待...")),
    (100, "最吉",
     ("100， 100诶！不用求人脉，好运自然来！", "好...好强！好事都会降临在你身边哦！")),
    (101, "？？？",
     ("？？？", "？？？"))
)


def luck_tip(val: int) -> tuple[str, str]:
    for index in range(len(luck_info) - 1):
        if luck_info[index][0] <= val < luck_info[index + 1][0]:
            return luck_info[index][1], random.choice(luck_info[index][2])
    return "Error", "Error"


def luck_generator(user_id: str) -> int:
    rand = random.Random()
    rand.seed(int(today()) + int(user_id) * random.randint(0, 6))
    return rand.randint(0, 100)


def get_average(values: list) -> tuple[int, float]:
    days = len(values)
    average = sum(values) / days
    return days, average


# command declarations
jrrp = on_alconna("jrrp", use_cmd_start=True, block=True, priority=5)
jrrp_week = on_alconna("jrrp.week", use_cmd_start=True, block=True, priority=5)
jrrp_month = on_alconna("jrrp.month", use_cmd_start=True, block=True, priority=5)
jrrp_year = on_alconna("jrrp.year", use_cmd_start=True, block=True, priority=5)
jrrp_all = on_alconna("jrrp.all", use_cmd_start=True, block=True, priority=5)


# command functions
@jrrp.handle()
async def jrrp_handler(session: Uninfo):
    user_id = session.user.id
    luck_val = db_conn.select_by_user_date(user_id)
    if luck_val == -1:
        luck_val = luck_generator(user_id)
        db_conn.insert(user_id, luck_val)
    short_info, long_info = luck_tip(luck_val)
    await UniMessage.text(f' 您今日的幸运值为{luck_val}， 为"{short_info}"。{long_info}').finish(at_sender=True)


@jrrp_week.handle()
async def jrrp_week_handler(session: Uninfo):
    user_id = session.user.id
    values = db_conn.select_by_range(user_id, SelectType.BY_WEEK)
    days, average = get_average(values)
    if days == 0:
        message = " 您本周还没有过幸运值记录哦~"
    else:
        message = f" 您本周总共有{days}条记录，平均幸运值为{average:.2f}。"
    await UniMessage.text(message).finish(at_sender=True)


@jrrp_month.handle()
async def jrrp_month_handler(session: Uninfo):
    user_id = session.user.id
    values = db_conn.select_by_range(user_id, SelectType.BY_MONTH)
    days, average = get_average(values)
    if days == 0:
        message = " 您本月还没有过幸运值记录哦~"
    else:
        message = f" 您本月总共有{days}条记录，平均幸运值为{average:.2f}。"
    await UniMessage.text(message).finish(at_sender=True)


@jrrp_year.handle()
async def jrrp_year_handler(session: Uninfo):
    user_id = session.user.id
    values = db_conn.select_by_range(user_id, SelectType.BY_YEAR)
    days, average = get_average(values)
    if days == 0:
        message = " 您今年还没有过幸运值记录哦~"
    else:
        message = f" 您今年总共有{days}条记录，平均幸运值为{average:.2f}。"
    await UniMessage.text(message).finish(at_sender=True)


@jrrp_all.handle()
async def jrrp_all_handler(session: Uninfo):
    user_id = session.user.id
    values = db_conn.select_by_range(user_id, SelectType.BY_NONE)
    days, average = get_average(values)
    if days == 0:
        message = " 您还没有过幸运值记录哦~"
    else:
        message = f" 您总共有{days}条记录，平均幸运值为{average:.2f}。"
    await UniMessage.text(message).finish(at_sender=True)

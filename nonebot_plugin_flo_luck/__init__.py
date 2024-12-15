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

from nonebot.plugin import PluginMetadata, inherit_supported_adapters

require("nonebot_plugin_alconna")
from nonebot_plugin_alconna import *

require("nonebot_plugin_uninfo")
from nonebot_plugin_uninfo import Uninfo

# ------------------------ import ------------------------

__plugin_meta__ = PluginMetadata(
    name="nonebot-plugin-flo-luck",
    description="",
    usage="",
    homepage="https://github.com/Florenz0707/nonebot-plugin-flo-luck",
    type="application",
    supported_adapters=inherit_supported_adapters(
        "nonebot_plugin_alconna", "nonebot_plugin_uninfo"
    ),
    config=Config,
    extra={
        "author": "florenz0707",
    }
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
     ("要不今天咱们就在床上躲一会吧...害怕...",
      "保佑。祝你平安。",
      "哎呀，你的幸运值几乎触底了！仿佛整个世界都在与你作对，每一步都充满荆棘。",
      "运势黑暗至极，仿佛被乌云笼罩，做任何事都如履薄冰，需万分小心。")),
    (1, "大凶",
     ("可能有人一直盯着你......",
      "要不今天咱还是别出门了......",
      "幸运值极低，仿佛被厄运之神紧紧盯住，每一个决定都可能引发连锁的不幸。",
      "运势如同陷入泥潭，每一步都异常艰难，需要极大的毅力和勇气才能挣脱困境。")),
    (10, "凶",
     ("啊这...昨天是不是做了什么不好的事？",
      "啊哈哈...或许需要多加小心呢。",
      "幸运值有所提升，但仍处于低谷，就像行走在薄冰上，随时可能陷入更深的困境。",
      "运势如同过山车，时好时坏，但大部分时间都在低谷徘徊，需保持警惕。")),
    (20, "末吉",
     ("呜呜，今天运气似乎不太好...",
      "勉强能算是个吉签吧。",
      "幸运值略有波动，但整体仍不理想，仿佛被无形的障碍阻挡，难以前进。",
      "运势如同迷雾中的航行，方向不明，每一步都充满未知和危险。")),
    (30, "末小吉",
     ("唔...今天运气有点差哦。",
      "今天喝水的时候务必慢一点。",
      "幸运值有所提升，但仍处于危险边缘，就像走在悬崖峭壁，一不小心就可能坠入深渊。",
      "运势如同暴风雨中的小船，随时可能被巨浪吞噬，需保持冷静和坚韧。")),
    (40, "小吉",
     ("还行吧，稍差一点点呢。",
      "差不多是阴天的水平吧，不用特别担心哦。",
      "幸运值开始有所好转，但仍需小心谨慎，因为稍有不慎就可能前功尽弃。",
      "运势如同黎明前的黑暗，虽然曙光初现，但仍需耐心等待和坚持。")),
    (50, "半吉",
     ("看样子是普通的一天呢。一切如常......",
      "加油哦！今天需要靠自己奋斗！",
      "终于摆脱了“不好”的厄运，运势开始稳步上升，但仍需继续努力才能保持势头。",
      "运势如同春日里的小草，虽然刚刚探出头来，但已经充满了生机和希望。")),
    (60, "吉",
     ("欸嘿...今天运气还不错哦？喜欢的博主或许会更新！",
      "欸嘿...今天运气还不错哦？要不去抽卡？",
      "幸运值大幅上升，仿佛被幸运之神眷顾，做什么都顺风顺水。",
      "运势如同夏日里的阳光，明媚而炽热，让人感受到无尽的温暖和力量。")),
    (70, "大吉",
     ("好耶！运气非常不错呢！今天是非常愉快的一天 ⌯>ᴗo⌯ .ᐟ.ᐟ",
      "好耶！大概是不经意间看见彩虹的程度吧？",
      "幸运值达到了巅峰状态，仿佛被金色的光环笼罩，无论做什么都能得到最好的结果。",
      "运势如同丰收的季节，硕果累累，让人感受到无尽的喜悦和满足。")),
    (80, "祥吉",
     ("哇哦！特别好运哦！无论是喜欢的事还是不喜欢的事都能全部解决！",
      "哇哦！特别好运哦！今天可以见到心心念念的人哦！",
      "幸运值几乎无人能敌，仿佛被宇宙的力量加持，做什么都能取得惊人的成就。",
      "运势如同璀璨的星空，每一颗星星都闪耀着耀眼的光芒，让人陶醉其中。")),
    (90, "佳吉",
     ("૮₍ˊᗜˋ₎ა 不用多说，怎么度过今天都会顺意的！",
      "૮₍ˊᗜˋ₎ა  会发生什么好事呢？真是期待...",
      "幸运值已经接近完美，仿佛被神明的庇佑所笼罩，做什么都能得心应手。",
      "运势如同梦幻般的仙境，每一个角落都充满了美好和奇迹。")),
    (100, "最吉",
     ("100， 100诶！不用求人脉，好运自然来！",
      "好...好强！好事都会降临在你身边哦！",
      "哇哦！你的幸运值已经达到了宇宙的极限！仿佛被全世界的幸福和美好所包围！",
      "恭喜你成为宇宙间最幸运的人！愿你的未来永远如同神话般绚烂多彩，好运与你同在！")),
    (0xff, "？？？",
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

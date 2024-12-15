# ------------------------ import ------------------------
# import packages from python
import random
from .database import *

# import packages from nonebot or other plugins
from nonebot import load_plugins, require
from nonebot.plugin import PluginMetadata, inherit_supported_adapters
from nonebot.permission import SUPERUSER

require("nonebot_plugin_alconna")
from nonebot_plugin_alconna import *

require("nonebot_plugin_uninfo")
from nonebot_plugin_uninfo import Uninfo

# ------------------------ import ------------------------

__plugin_meta__ = PluginMetadata(
    name="nonebot-plugin-flo-luck",
    description="Florenz 版本的 jrrp， 主要追加了特殊列表与排行功能。",
    usage="""==============用户使用==============
    1> jrrp 查看今日幸运值。
    2> jrrp.week (month|year|all) 查看平均幸运值。
    3> jrrp.rank 查看自己的幸运值在今日的排行。
    ============超级用户使用============
    4> jrrp.add user_id [-g greeting] [-b bottom] [-t top] 
       将QQ号为user_id的用户加入特殊列表，问候语为greeting，幸运值取值为[bottom, top]。
       默认无问候语，取值[0, 100]。
    5> jrrp.del user_id 将用户移出特殊列表。
    6> jrrp.check 查看当前特殊列表。
    """,
    homepage="https://github.com/Florenz0707/nonebot-plugin-flo-luck",
    type="application",
    supported_adapters=inherit_supported_adapters(
        "nonebot_plugin_alconna", "nonebot_plugin_uninfo"
    ),
    extra={
        "author": "florenz0707",
    }
)

sub_plugins = load_plugins(
    str(Path(__file__).parent.joinpath("plugins").resolve())
)

luck_conn = LuckDataBase()
sp_conn = SpecialDataBase()

# format: (val: int, short_info: str, (long_info_1: str, long_info_2, ...))
luck_info = (
    (0, "最凶",
     ("要不今天咱们就在床上躲一会吧...害怕...",
      "保佑。祝你平安。",
      "哎呀，幸运值几乎触底了！整个世界都在与你作对，每一步都充满荆棘。",
      "运势黑暗至极，做任何事都如履薄冰，需万分小心。")),
    (1, "大凶",
     ("可能有人一直盯着你......",
      "要不今天咱还是别出门了......",
      "幸运值极低，被厄运之神紧紧盯住，每一个决定都可能引发连锁的不幸。",
      "运势陷入泥潭，需要极大的毅力和勇气才能挣脱困境。")),
    (10, "凶",
     ("啊这...昨天是不是做了什么不好的事？",
      "啊哈哈...或许需要多加小心呢。",
      "幸运值有所提升，但仍处于低谷，随时可能陷入更深的困境。",
      "运势如同过山车，时好时坏，但大部分时间都在低谷徘徊，保持警惕。")),
    (20, "末吉",
     ("呜呜，今天运气似乎不太好...",
      "勉强能算是个吉签吧。",
      "幸运值略有波动，但整体仍不理想，仿佛被无形的障碍阻挡。",
      "迷雾中的航行，方向不明。")),
    (30, "末小吉",
     ("唔...今天运气有点差哦。",
      "今天喝水的时候务必慢一点。",
      "幸运值有所提升，但仍处于危险边缘。",
      "暴风雨中的小船，随时可能被巨浪吞噬，需保持冷静和坚韧。")),
    (40, "小吉",
     ("还行吧，稍差一点点呢。",
      "差不多是阴天的水平吧，不用特别担心哦。",
      "幸运值开始有所好转，但仍需小心谨慎，因为稍有不慎就可能前功尽弃。",
      "黎明前的黑暗，虽然曙光初现，但仍需耐心等待和坚持。")),
    (50, "半吉",
     ("看样子是普通的一天呢。一切如常......",
      "加油哦！今天需要靠自己奋斗！",
      "终于摆脱了厄运，运势开始稳步上升，继续努力才能保持势头。",
      "运势如同春日里的小草，虽然刚刚探出头来，但已经充满了生机和希望。")),
    (60, "吉",
     ("欸嘿...今天运气还不错哦？喜欢的博主或许会更新！",
      "欸嘿...今天运气还不错哦？要不去抽卡？",
      "幸运值大幅上升，幸运之神眷顾，做什么都顺风顺水。",
      "运势如同夏日里的阳光，明媚而炽热，让人感受到无尽的温暖和力量。")),
    (70, "大吉",
     ("好耶！运气非常不错呢！今天是非常愉快的一天 ⌯>ᴗo⌯ .ᐟ.ᐟ",
      "好耶！大概是不经意间看见彩虹的程度吧？",
      "金色光环笼罩，无论做什么都能得到最好的结果。",
      "丰收的季节，硕果累累，让人感受到无尽的喜悦和满足。")),
    (80, "祥吉",
     ("哇哦！特别好运哦！无论是喜欢的事还是不喜欢的事都能全部解决！",
      "哇哦！特别好运哦！今天可以见到心心念念的人哦！",
      "幸运几乎无人能敌，宇宙力量加持，做什么都能取得惊人的成就。",
      "璀璨的星空，每一颗星星都闪耀着耀眼的光芒，让人陶醉其中。")),
    (90, "佳吉",
     ("૮₍ˊᗜˋ₎ა 不用多说，今天怎么度过都会顺意的！",
      "૮₍ˊᗜˋ₎ა  会发生什么好事呢？真是期待...",
      "幸运值已经接近完美，神明庇佑，做什么都能得心应手。",
      "梦幻般的仙境，每一个角落都充满了美好和奇迹。")),
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

    logger.error(f"Unexpected value {val}")
    return "Error", "Error"


def luck_generator(user_id: str, bottom: int = 0, top: int = 100) -> int:
    rand = random.Random()
    rand.seed(int(today()) + int(user_id) * random.randint(0, 6))
    return rand.randint(bottom, top)


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
jrrp_rank = on_alconna("jrrp.rank", use_cmd_start=True, block=True, priority=5)
jrrp_add = on_alconna(
    Alconna(
        "jrrp.add",
        Args["target?", str],
        Option("-g", Args["greeting", str]),
        Option("-b", Args["bottom", int]),
        Option("-t", Args["top", int]),
    ),
    use_cmd_start=True,
    block=True,
    priority=5,
    permission=SUPERUSER
)
jrrp_del = on_alconna(
    Alconna(
        "jrrp.del",
        Args["target?", str]
    ),
    use_cmd_start=True,
    block=True,
    priority=5,
    permission=SUPERUSER
)
jrrp_check = on_alconna("jrrp.check", use_cmd_start=True, block=True, priority=5, permission=SUPERUSER)


# command functions
@jrrp.handle()
async def jrrp_handler(session: Uninfo):
    user_id = session.user.id
    luck_val = luck_conn.select_by_user_date(user_id)
    bottom, top = 0, 100
    if (info := sp_conn.select_by_user(user_id)) is not None:
        bottom, top = info[1], info[2]
        if info[0] != "":
            await UniMessage.text(info[0]).send()
    if luck_val == -1:
        luck_val = luck_generator(user_id, bottom, top)
        luck_conn.insert(user_id, luck_val)
    short_info, long_info = luck_tip(luck_val)
    await UniMessage.text(f' 您今日的幸运值为{luck_val}， 为"{short_info}"。{long_info}').finish(at_sender=True)


@jrrp_week.handle()
async def jrrp_week_handler(session: Uninfo):
    user_id = session.user.id
    values = luck_conn.select_by_range(user_id, SelectType.BY_WEEK)
    days, average = get_average(values)
    if days == 0:
        message = " 您本周还没有过幸运值记录哦~"
    else:
        message = f" 您本周总共有{days}条记录，平均幸运值为{average:.2f}。"
    await UniMessage.text(message).finish(at_sender=True)


@jrrp_month.handle()
async def jrrp_month_handler(session: Uninfo):
    user_id = session.user.id
    values = luck_conn.select_by_range(user_id, SelectType.BY_MONTH)
    days, average = get_average(values)
    if days == 0:
        message = " 您本月还没有过幸运值记录哦~"
    else:
        message = f" 您本月总共有{days}条记录，平均幸运值为{average:.2f}。"
    await UniMessage.text(message).finish(at_sender=True)


@jrrp_year.handle()
async def jrrp_year_handler(session: Uninfo):
    user_id = session.user.id
    values = luck_conn.select_by_range(user_id, SelectType.BY_YEAR)
    days, average = get_average(values)
    if days == 0:
        message = " 您今年还没有过幸运值记录哦~"
    else:
        message = f" 您今年总共有{days}条记录，平均幸运值为{average:.2f}。"
    await UniMessage.text(message).finish(at_sender=True)


@jrrp_all.handle()
async def jrrp_all_handler(session: Uninfo):
    user_id = session.user.id
    values = luck_conn.select_by_range(user_id, SelectType.BY_NONE)
    days, average = get_average(values)
    if days == 0:
        message = " 您还没有过幸运值记录哦~"
    else:
        message = f" 您总共有{days}条记录，平均幸运值为{average:.2f}。"
    await UniMessage.text(message).finish(at_sender=True)


@jrrp_rank.handle()
async def jrrp_rank_handler(session: Uninfo):
    user_id = session.user.id
    if luck_conn.select_by_user_date(user_id) == -1:
        await UniMessage.text(" 您今日还没有幸运值哦~先开启幸运值再查看排名吧！").finish(at_sender=True)
    today_total = luck_conn.select_by_date()
    today_total.sort(key=(lambda item: item[1]), reverse=True)
    for index in range(len(today_total)):
        if today_total[index][0] == user_id:
            await UniMessage.text(f" 您的幸运值是{today_total[index][1]}，"
                                  f"在今日的排名中目前位于 {index + 1} / {len(today_total)}。").finish()


@jrrp_add.handle()
async def jrrp_add_handler(
        user_id: Match[str] = AlconnaMatch("target"),
        greeting: Query[str] = Query("greeting", ""),
        bottom: Query[int] = Query("bottom", 0),
        top: Query[int] = Query("top", 100)):
    if user_id.available and greeting.available and bottom.available and top.available:
        user_id = user_id.result
        greeting = greeting.result
        bottom = min(bottom.result, 0)
        top = max(top.result, 100)
        if sp_conn.insert(user_id, greeting, bottom, top):
            message = f"""
成功插入数据：
user_id: {user_id}, 
greeting: '{greeting}', 
bottom: {bottom}, 
top: {top}"""
        else:
            message = f" 表中已存在条目'{user_id}'，插入失败。"
    else:
        message = " 参数无效。"

    await UniMessage.text(message).finish(at_sender=True)


@jrrp_del.handle()
async def jrrp_del_handler(user_id: Match[str] = AlconnaMatch("target")):
    if user_id.available:
        user_id = user_id.result
        if (old_info := sp_conn.select_by_user(user_id)) is None:
            message = f" 删除失败，表中不存在条目'{user_id}'。"
        else:
            sp_conn.remove(user_id)
            message = f"""
删除成功，原数据：
user_id: {user_id}, 
greeting: '{old_info[0]}', 
bottom: {old_info[1]}, 
top: {old_info[2]}"""
    else:
        message = " 参数无效。"
    await UniMessage.text(message).finish(at_sender=True)


@jrrp_check.handle()
async def jrrp_check_handler():
    items = sp_conn.select_all()
    await UniMessage.text(f"共有{len(items)}条数据。").send()
    if len(items) != 0:
        message = ""
        for item in items:
            message += f"""
user_id: {item[0]},
greeting: '{item[1]}',
bottom: {item[2]},
top: {item[3]}
"""
        await UniMessage.text(message).finish(at_sender=True)

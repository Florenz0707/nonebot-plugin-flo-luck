# ------------------------ import ------------------------
# import packages from python
from pathlib import Path
from datetime import date
import random

# import packages from nonebot or other plugins
from nonebot import get_plugin_config, load_plugins, require
from nonebot.plugin import PluginMetadata
from .config import Config

require("nonebot_plugin_alconna")
from nonebot_plugin_alconna import *

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

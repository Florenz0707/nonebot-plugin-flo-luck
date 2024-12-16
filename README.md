<div align="center">
  <a href="https://v2.nonebot.dev/store"><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo"></a>
  <br>
  <p><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/NoneBotPlugin.svg" width="240" alt="NoneBotPluginText"></p>
</div>

<div align="center">

# nonebot-plugin-flo-luck

_✨ NoneBot 插件: Florenz 版本的 jrrp ✨_


<a href="./LICENSE">
    <img src="https://img.shields.io/github/license/florenz0707/nonebot-plugin-flo-luck.svg" alt="license">
</a>
<a href="https://pypi.python.org/pypi/nonebot-plugin-flo-luck">
    <img src="https://img.shields.io/pypi/v/nonebot-plugin-flo-luck.svg" alt="pypi">
</a>
<img src="https://img.shields.io/badge/python-3.9+-blue.svg" alt="python">

</div>



## 📖 介绍

Florenz 版本的 jrrp。主要追加了特殊列表与排行功能。  
列表内容：QQ号，该用户使用时发送的特别问候，该用户幸运值的下限和上限。  

## 💿 安装

<details open>
<summary>使用 nb-cli 安装</summary>
在 nonebot2 项目的根目录下打开命令行, 输入以下指令即可安装

    nb plugin install nonebot-plugin-flo-luck

</details>

<details>
<summary>使用包管理器安装</summary>
在 nonebot2 项目的插件目录下, 打开命令行, 根据你使用的包管理器, 输入相应的安装命令

<details>

<summary>pip</summary>

    pip install nonebot-plugin-flo-luck
</details>

<details>
<summary>poetry</summary>

    poetry add nonebot-plugin-flo-luck
</details>

打开 nonebot2 项目根目录下的 `pyproject.toml` 文件, 在 `[tool.nonebot]` 部分追加写入

    plugins = ["nonebot_plugin_flo_luck"]

</details>

## ⚙️ 配置

无

## 🎉 使用
### 指令表
|             指令              |    权限     | 需要@ | 范围 |             说明              |
|:---------------------------:|:---------:|:---:|:--:|:---------------------------:|
|            jrrp             |    所有     |  否  | 所有 |           查看今日人品            |
| jrrp.week  (month/year/all) |    所有     |  否  | 所有 |           查看平均人品            |
|       jrrp.add/del id       | SUPERUSER |  否  | 所有 | 从特殊列表中加入/移除该QQ  （具体参数请看元数据） |
|         jrrp.check          | SUPERUSER |  否  | 所有 |          查看特殊列表内容           |
|          jrrp.rank          |    所有     |  否  | 所有 |       查看自己的幸运值在今日的排行        |
### 其他
大部分代码源于：[nonebot-plugin-jrrp2](https://github.com/Rene8028/nonebot_plugin_jrrp2)  
本插件主要增加了特殊列表与排行功能  
Version: 0.1.2
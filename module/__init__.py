# coding=UTF-8
# Author:LZY/我不是盘神
# Software:PyCharm
# Time:2023/11/18 12:28:18
# File:__init__.py.py
import os
from loguru import logger
from pyrogram import utils


# v1.1.2 解决链接若附带/c字段即私密频道无法下载的问题,是由于pyrogram的问题:https://github.com/pyrogram/pyrogram/issues/1314
def get_peer_type_new(peer_id: int) -> str:
    peer_id_str = str(peer_id)
    if not peer_id_str.startswith("-"):
        return "user"
    elif peer_id_str.startswith("-100"):
        return "channel"
    else:
        return "chat"


utils.get_peer_type = get_peer_type_new
__version__ = '1.1.6'
__license__ = "MIT License"
__copyright__ = "Copyright (C) 2024 Gentlesprite <https://github.com/Gentlesprite>"
__update_date__ = '2024/11/17 15:33:12'
SOFTWARE_FULL_NAME = 'Telegram Restricted Media Downloader'
SOFTWARE_NAME = 'TRMD'
author = 'Gentlesprite'
LOG_PATH = os.path.join(os.environ['APPDATA'], SOFTWARE_NAME, f'{SOFTWARE_NAME}_LOG.log')
# 配置日志输出到文件
logger.add(sink=LOG_PATH, level='INFO', rotation='10 MB', retention='10 days', compression='zip', encoding='UTF-8',
           enqueue=True)

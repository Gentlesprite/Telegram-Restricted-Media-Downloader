# coding=UTF-8
# Author:LZY/我不是盘神
# Software:PyCharm
# Time:2023/11/18 12:28:18
# File:__init__.py.py
import os
from loguru import logger

__version__ = '1.1.0'
__license__ = "MIT License"
__copyright__ = "Copyright (C) 2024 Gentlesprite <https://github.com/Gentlesprite>"
__update_date__ = '2024/09/06 19:54:08'
SOFTWARE_FULL_NAME = 'Telegram Restricted Media Downloader'
SOFTWARE_NAME = 'TRMD'
author = 'Gentlesprite'
LOG_PATH = os.path.join(os.environ['APPDATA'], SOFTWARE_NAME, 'TRMD_LOG.log')
# 配置日志输出到文件
logger.add(sink=LOG_PATH, level='INFO', rotation='10 MB', retention='10 days', compression='zip', encoding='UTF-8',
           enqueue=True)

# coding=UTF-8
# Author:LZY/我不是盘神
# Software:PyCharm
# Time:2023/11/18 12:28:18
# File:__init__.py
import os
import sys
import yaml
import atexit
import readline
import datetime
import mimetypes
from ctypes import windll
from loguru import logger
from pyrogram import utils
from rich.console import Console
from typing import Tuple, List, Dict, Any, Optional


# v1.1.2 解决链接若附带/c字段即私密频道无法下载的问题,是由于pyrogram的问题:https://github.com/pyrogram/pyrogram/issues/1314
def get_peer_type_new(peer_id: int) -> str:
    peer_id_str = str(peer_id)
    if not peer_id_str.startswith("-"):
        return "user"
    elif peer_id_str.startswith("-100"):
        return "channel"
    else:
        return "chat"


def read_input_history(history_path: str, max_record_len: int):
    # 尝试读取历史记录文件
    try:
        readline.read_history_file(history_path)
    except FileNotFoundError:
        pass
    # 设置历史记录的最大长度
    readline.set_history_length(max_record_len)
    # 注册退出时保存历史记录
    atexit.register(readline.write_history_file, history_path)


def check_run_env():  # 检测是控制台运行还是IDE运行
    return windll.kernel32.SetConsoleTextAttribute(windll.kernel32.GetStdHandle(-0xb), 0x7)


# 自定义 yaml文件中 None 的表示
class CustomDumper(yaml.Dumper):
    def represent_none(self, data):
        return self.represent_scalar('tag:yaml.org,2002:null', '~')


console = Console()
utils.get_peer_type = get_peer_type_new
__version__ = '1.1.7'
__license__ = "MIT License"
__copyright__ = "Copyright (C) 2024 Gentlesprite <https://github.com/Gentlesprite>"
__update_date__ = '2024/11/29 10:20:53'
SOFTWARE_FULL_NAME = 'Telegram Restricted Media Downloader'
SOFTWARE_NAME = 'TRMD'
author = 'Gentlesprite'
APPDATA_PATH = os.path.join(os.environ['APPDATA'], SOFTWARE_NAME)
LOG_PATH = os.path.join(APPDATA_PATH, f'{SOFTWARE_NAME}_LOG.log')
INPUT_HISTORY_PATH = os.path.join(APPDATA_PATH, f'.{SOFTWARE_NAME}_HISTORY')
MAX_RECORD_LENGTH = 1000
read_input_history(history_path=INPUT_HISTORY_PATH, max_record_len=MAX_RECORD_LENGTH)
# 配置日志输出到文件
logger.add(sink=LOG_PATH, level='INFO', rotation='10 MB', retention='10 days', compression='zip', encoding='UTF-8',
           enqueue=True)
CustomDumper.add_representer(type(None), CustomDumper.represent_none)

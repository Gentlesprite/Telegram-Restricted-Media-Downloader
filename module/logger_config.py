# coding=UTF-8
# Author:Gentlesprite
# Software:PyCharm
# Time:2024/7/22 16:39
# File:logger_config
from loguru import logger

import module.enum_define
from module.__init__ import SOFTWARE_NAME
from scprint import print as print_color
import os

LOG_PATH = os.path.join(os.environ['APPDATA'], SOFTWARE_NAME, 'TRMD_LOG.log')


def setup_no_console_loger_config() -> None:
    logger.remove(handler_id=None)
    # 配置日志输出到文件
    logger.add(sink=LOG_PATH, level='INFO', rotation='00:00', retention='3 days', compression='zip', encoding='UTF-8',
               enqueue=True)


def print_with_log(msg: str, level: module.enum_define.LogLevel) -> None:
    getattr(logger, level.text)(msg)
    print_color(msg, color=level.color.text)

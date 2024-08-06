# coding=UTF-8
# Author:Gentlesprite
# Software:PyCharm
# Time:2024/7/22 16:39
# File:logger_config
import os
import module.enum_define
from loguru import logger
from scprint import print as print_color
from module.__init__ import SOFTWARE_NAME
from datetime import datetime

LOG_PATH = os.path.join(os.environ['APPDATA'], SOFTWARE_NAME, 'TRMD_LOG.log')


def setup_no_console_loger_config() -> None:
    logger.remove(handler_id=None)  # 关闭终端日志显示
    # 配置日志输出到文件
    logger.add(sink=LOG_PATH, level='INFO', rotation='10 MB', retention='10 days', compression='zip', encoding='UTF-8',
               enqueue=True)


def print_with_log(msg: str, level: module.enum_define.LogLevel) -> None:
    try:
        getattr(logger, level.text)(msg)

        print_color(
            f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} | {getattr(level,"translate_text")} | {msg}',
            color=level.color.text)
    except UnicodeEncodeError as e:
        getattr(logger, level.text)(f'彩色打印发生错误！原因:{e}')
        print(msg)

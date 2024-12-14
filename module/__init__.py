# coding=UTF-8
# Author:LZY/我不是盘神
# Software:PyCharm
# Time:2023/11/18 12:28:18
# File:__init__.py
import os
import sys
import yaml
import atexit
import shutil
import readline
import pyrogram
import logging
import datetime
import mimetypes
from pyrogram.errors import FloodWait
from pyrogram.errors.exceptions.bad_request_400 import MsgIdInvalid, UsernameInvalid
from pyrogram.errors.exceptions.unauthorized_401 import SessionRevoked, AuthKeyUnregistered, SessionExpired
from ctypes import windll
from rich.console import Console
from rich.logging import RichHandler
from logging import Formatter
from logging.handlers import RotatingFileHandler
from pyrogram import utils
from typing import Tuple, List, Set, Dict, Any, Optional


class TelegramRestrictedMediaDownloaderClient(pyrogram.Client):

    async def authorize(self) -> pyrogram.types.User:
        if self.bot_token:
            return await self.sign_in_bot(self.bot_token)
        console.print(
            f'Pyrogram is free software and comes with ABSOLUTELY NO WARRANTY. Licensed\n'
            f'under the terms of the {pyrogram.__license__}.')
        console.print(
            f'欢迎使用[#b4009e]{SOFTWARE_FULL_NAME}[/#b4009e](版本 {__version__})'
            f'基于Pyrogram(版本 {pyrogram.__version__})。')
        while True:
            try:
                if not self.phone_number:
                    while True:
                        value = console.input('请输入「电话号码」或「bot token」([#6a2c70]电话号码[/#6a2c70]需以[#b83b5e]「+地区」'
                                              '[/#b83b5e]开头!如:[#f08a5d]+86[/#f08a5d][#f9ed69]15000000000[/#f9ed69]):')
                        if not value:
                            continue

                        confirm = console.input(f'所输入的「{value}」是否[green]正确[/green]? - 「y|n」(默认y): ').lower()

                        if confirm == 'y' or confirm == '':
                            break
                        else:
                            log.warning(f'意外的参数:"{confirm}",支持的参数 - 「y|n」(默认y)')
                    if ":" in value:
                        self.bot_token = value
                        return await self.sign_in_bot(value)
                    else:
                        self.phone_number = value

                sent_code = await self.send_code(self.phone_number)
            except pyrogram.errors.BadRequest as e:
                console.print(e.MESSAGE)
                self.phone_number = None
                self.bot_token = None
            else:
                break

        sent_code_descriptions = {
            pyrogram.enums.SentCodeType.APP: 'Telegram app',
            pyrogram.enums.SentCodeType.SMS: 'SMS',
            pyrogram.enums.SentCodeType.CALL: 'phone call',
            pyrogram.enums.SentCodeType.FLASH_CALL: 'phone flash call',
            pyrogram.enums.SentCodeType.FRAGMENT_SMS: 'Fragment SMS',
            pyrogram.enums.SentCodeType.EMAIL_CODE: 'email code'
        }

        console.print(f'「验证码」已通过「{sent_code_descriptions[sent_code.type]}」发送。')

        while True:
            if not self.phone_code:
                self.phone_code = console.input('请输入收到的「验证码」:')

            try:
                signed_in = await self.sign_in(self.phone_number, sent_code.phone_code_hash, self.phone_code)
            except pyrogram.errors.BadRequest as e:
                console.print(e.MESSAGE)
                self.phone_code = None
            except pyrogram.errors.SessionPasswordNeeded as e:
                console.print(e.MESSAGE)

                while True:
                    console.print('密码提示:{}'.format(await self.get_password_hint()))

                    if not self.password:
                        self.password = console.input('输入「密码」(为空代表恢复密码):', password=self.hide_password)

                    try:
                        if not self.password:
                            confirm = console.input('确认「恢复密码」? - 「y|n」(默认y):').lower()

                            if confirm == 'y' or confirm == '':
                                email_pattern = await self.send_recovery_code()
                                console.print(f'「恢复代码」已发送到「{email_pattern}」。')

                                while True:
                                    recovery_code = console.input('请输入「恢复代码」:')

                                    try:
                                        return await self.recover_password(recovery_code)
                                    except pyrogram.errors.BadRequest as e:
                                        console.print(e.MESSAGE)
                                    except Exception as e:
                                        console.print_exception()
                                        raise
                            else:
                                self.password = None
                        else:
                            return await self.check_password(self.password)
                    except pyrogram.errors.BadRequest as e:
                        console.print(e.MESSAGE)
                        self.password = None
            else:
                break

        if isinstance(signed_in, pyrogram.types.User):
            return signed_in

        while True:
            first_name = console.input('输入「名字」:')
            last_name = console.input('输入「姓氏」(为空代表跳过): ')

            try:
                signed_up = await self.sign_up(
                    self.phone_number,
                    sent_code.phone_code_hash,
                    first_name,
                    last_name
                )
            except pyrogram.errors.BadRequest as e:
                console.print(e.MESSAGE)
            else:
                break

        if isinstance(signed_in, pyrogram.types.TermsOfService):
            console.print('\n' + signed_in.text + '\n')
            await self.accept_terms_of_service(signed_in.id)

        return signed_up


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


console = Console(log_path=False)
utils.get_peer_type = get_peer_type_new
__version__ = '1.2.4'
__license__ = "MIT License"
__update_date__ = '2024/12/15 03:06:54'
__copyright__ = f'Copyright (C) {__update_date__[:4]} Gentlesprite <https://github.com/Gentlesprite>'
SOFTWARE_FULL_NAME = 'Telegram Restricted Media Downloader'
SOFTWARE_NAME = 'TRMD'
author = 'Gentlesprite'
APPDATA_PATH = os.path.join(os.environ['APPDATA'], SOFTWARE_NAME)
INPUT_HISTORY_PATH = os.path.join(APPDATA_PATH, f'.{SOFTWARE_NAME}_HISTORY')
MAX_RECORD_LENGTH = 1000
read_input_history(history_path=INPUT_HISTORY_PATH, max_record_len=MAX_RECORD_LENGTH)

# 配置日志输出到文件
LOG_PATH = os.path.join(APPDATA_PATH, f'{SOFTWARE_NAME}_LOG.log')
MAX_LOG_SIZE = 3 * 1024 * 1024  # 3 MB
BACKUP_COUNT = 3  # 保留最近3个日志文件

# 配置日志文件处理器（支持日志轮换）
file_handler = RotatingFileHandler(
    filename=LOG_PATH, maxBytes=MAX_LOG_SIZE, backupCount=BACKUP_COUNT
)
file_handler.setFormatter(logging.Formatter("%(message)s"))
# 配置日志记录器
logging.basicConfig(
    level=logging.WARNING,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[
        RichHandler(rich_tracebacks=True),  # 终端输出
        file_handler  # 文件输出
    ]
)
log = logging.getLogger('rich')

CustomDumper.add_representer(type(None), CustomDumper.represent_none)

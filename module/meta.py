# coding=UTF-8
# Author:LZY/我不是盘神
# Software:PyCharm
# Time:2023/12/14 18:36:14
# File:print_meta.py
"""Utility module to manage meta info."""
import platform

from rich.console import Console

from . import __copyright__, __license__, __version__, SOFTWARE_FULL_NAME
from .enum_define import LogLevel

APP_VERSION = f"{SOFTWARE_FULL_NAME} {__version__}"
DEVICE_MODEL = f"{platform.python_implementation()} {platform.python_version()}"
SYSTEM_VERSION = f"{platform.system()} {platform.release()}"
LANG_CODE = "zh"


def print_meta(printer):
    """Prints meta-data of the downloader script."""
    console = Console()
    # pylint: disable = C0301
    console.log(
        f"[bold]{SOFTWARE_FULL_NAME} v{__version__}[/bold],\n[i]{__copyright__}[/i]"
    )
    console.log(f"Licensed under the terms of the {__license__}", end="\n\n")
    console.log('软件完全免费使用！禁止倒卖,如果你付费那就是被骗了。')
    printer(f"Device: {DEVICE_MODEL} - {APP_VERSION}", level=LogLevel.info)
    printer(f"System: {SYSTEM_VERSION} ({LANG_CODE.upper()})", level=LogLevel.info)

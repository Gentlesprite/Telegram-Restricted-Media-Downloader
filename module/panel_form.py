# coding=UTF-8
# Author:LZY/我不是盘神
# Software:PyCharm
# Time:2024/1/2 17:43:02
# File:panel_form.py
from enum import Enum
from prettytable import PrettyTable
from ctypes import windll


class StatusInfo(Enum):
    skip = 1
    success = 2
    failure = 3
    downloading = 4


class MediaType(Enum):
    video = 1
    photo = 2
    unknown = 3


class StorageType(Enum):
    single = 1
    group = 2


def translate_storage_type(stype: StorageType):
    if stype == StorageType.single:
        stype = '单文件'
    elif stype == StorageType.group:
        stype = '组'
    return stype


def translate_media_type(name: MediaType):
    if name == MediaType.video:
        name = '视频'
    elif name == MediaType.photo:
        name = '图片'
    elif name == MediaType.unknown:
        name = '未知'
    return name


def translate_link_status(status: StatusInfo, image_display=False):
    if status == StatusInfo.skip:
        status = '⏭️' if image_display and check_run_env() else '跳过'
    elif status == StatusInfo.success:
        status = '✅' if image_display and check_run_env() else '成功'
    elif status == StatusInfo.failure:
        status = '❌' if image_display and check_run_env() else '失败'
    elif status == StatusInfo.downloading:
        status = '⬇️' if image_display and check_run_env() else '下载中'
    return status


class PanelTable:
    def __init__(self, title: str, header: tuple, data=None):
        self.table = PrettyTable(title=title, field_names=header)
        self.add_row(data) if data else None

    def add_row(self, data):
        self.table.add_rows([data])

    def print_meta(self):
        print(self.table)


def check_run_env():  # 检测是控制台运行还是IDE运行
    return windll.kernel32.SetConsoleTextAttribute(windll.kernel32.GetStdHandle(-0xb), 0x7)


# coding=UTF-8
# Author:Gentlesprite
# Software:PyCharm
# Time:2024/7/2 0:59
# File:enum_define.py
from enum import Enum


class LinkType(Enum):
    single = 0
    group = 1
    include_comment = 2

    @property
    def text(self):
        return {
            LinkType.single: '单文件',
            LinkType.group: '组',
            LinkType.include_comment: '包含评论',
        }[self]


class DownloadStatus(Enum):
    downloading = 0
    success = 1
    failure = 2
    skip = 3
    all_complete = 4

    @property
    def text(self):
        return {
            DownloadStatus.downloading: '下载中',
            DownloadStatus.success: '下载成功',
            DownloadStatus.failure: '下载失败',
            DownloadStatus.skip: '跳过下载',
            DownloadStatus.all_complete: '全部下载完成'
        }[self]


class KeyWorld(Enum):
    link = 0
    link_type = 1
    id = 2
    size = 3
    status = 4
    file = 5
    error_size = 6
    actual_size = 7

    @property
    def text(self):
        return {
            KeyWorld.link: '链接',
            KeyWorld.link_type: '链接类型',
            KeyWorld.id: '标识',
            KeyWorld.size: '大小',
            KeyWorld.status: '状态',
            KeyWorld.file: '文件',
            KeyWorld.error_size: '错误大小',
            KeyWorld.actual_size: '实际大小'
        }[self]


class LogLevel(Enum):
    debug = 0
    info = 1
    success = 2
    warning = 3
    error = 4

    @property
    def text(self):
        return {
            LogLevel.debug: 'debug',
            LogLevel.info: 'info',
            LogLevel.success: 'success',
            LogLevel.warning: 'warning',
            LogLevel.error: 'error'
        }[self]

    @property
    def color(self):
        color_mapping = {
            LogLevel.debug: PrintColor.blue,
            LogLevel.info: PrintColor.white,
            LogLevel.success: PrintColor.green,
            LogLevel.warning: PrintColor.yellow,
            LogLevel.error: PrintColor.red
        }
        return color_mapping.get(self, PrintColor.white)


class PrintColor(Enum):
    blue = 0
    white = 1
    green = 2
    yellow = 3
    red = 4



    @property
    def text(self):
        return {
            PrintColor.blue: 'blue',
            PrintColor.white: 'white',
            PrintColor.green: 'green',
            PrintColor.yellow: 'yellow',
            PrintColor.red: 'red',
            PrintColor.violet: 'violet'
        }[self]

    @classmethod
    def violet(cls):
        return cls(6)

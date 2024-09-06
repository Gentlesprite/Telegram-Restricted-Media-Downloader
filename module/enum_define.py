# coding=UTF-8
# Author:Gentlesprite
# Software:PyCharm
# Time:2024/7/2 0:59
# File:enum_define.py
from enum import Enum


class LinkType(Enum):
    single = 0
    group = 1
    comment = 2

    @property
    def text(self):
        return {
            LinkType.single: 'single',
            LinkType.group: 'group',
            LinkType.comment: 'comment',
        }[self]

    @staticmethod
    def translate(text: 'LinkType.text'):
        translation = {
            LinkType.single.text: '单文件',
            LinkType.group.text: '组文件',
            LinkType.comment.text: '评论文件',
        }
        if text in translation:
            return translation[text]
        else:
            raise ValueError(f'Unsupported Keyword:{text}')


class DownloadType(Enum):
    video = 0
    photo = 1

    @property
    def text(self):
        return {
            DownloadType.video: 'video',
            DownloadType.photo: 'photo'
        }[self]

    @staticmethod
    def support_type() -> list:
        return [i.text for i in DownloadType]

    @staticmethod
    def translate(text: 'DownloadType.text'):
        translation = {
            DownloadType.video.text: '视频',
            DownloadType.photo.text: '图片'
        }
        if text in translation:
            return translation[text]
        else:
            raise ValueError(f'Unsupported Keyword:{text}')


class DownloadStatus(Enum):
    downloading = 0
    success = 1
    failure = 2
    skip = 3
    all_complete = 4

    @property
    def text(self):
        return {
            DownloadStatus.downloading: 'downloading',
            DownloadStatus.success: 'success',
            DownloadStatus.failure: 'failure',
            DownloadStatus.skip: 'skip'
        }[self]

    @staticmethod
    def translate(text: 'DownloadStatus.text'):
        translation = {
            DownloadStatus.downloading.text: '正在下载',
            DownloadStatus.success.text: '成功下载',
            DownloadStatus.failure.text: '失败下载',
            DownloadStatus.skip.text: '跳过下载'
        }
        if text in translation:
            return translation[text]
        else:
            print(text)
            raise ValueError(f'Unsupported Keyword:{text}')

    @staticmethod
    def all_status() -> list:
        return [i.text for i in DownloadStatus]


class KeyWorld(Enum):
    link = 0
    link_type = 1
    id = 2
    size = 3
    status = 4
    file = 5
    error_size = 6
    actual_size = 7
    already_exist = 8
    chanel = 9
    type = 10
    download_task_error = 11

    @property
    def text(self):
        return {
            KeyWorld.link: 'link',
            KeyWorld.link_type: 'link_type',
            KeyWorld.id: 'id',
            KeyWorld.size: 'size',
            KeyWorld.status: 'status',
            KeyWorld.file: 'file',
            KeyWorld.error_size: 'error_size',
            KeyWorld.actual_size: 'actual_size',
            KeyWorld.already_exist: 'already_exist',
            KeyWorld.chanel: 'chanel',
            KeyWorld.type: 'type',
            KeyWorld.download_task_error: 'download_task_error'
        }[self]

    @staticmethod
    def translate(text: 'KeyWorld.text', key_note: bool = False):
        translation = {
            KeyWorld.link.text: '链接',
            KeyWorld.link_type.text: '链接类型',
            KeyWorld.id.text: '标识',
            KeyWorld.size.text: '大小',
            KeyWorld.status.text: '状态',
            KeyWorld.file.text: '文件',
            KeyWorld.error_size.text: '错误大小',
            KeyWorld.actual_size.text: '实际大小',
            KeyWorld.already_exist.text: '已存在',
            KeyWorld.chanel.text: '频道',
            KeyWorld.type.text: '类型',
            KeyWorld.download_task_error.text: '下载任务错误'
        }

        if text in translation:
            if key_note:
                return f'[{translation[text]}]'
            else:
                return translation[text]
        else:
            raise ValueError(f'Unsupported Keyword:{text}')


class StatusInfo(Enum):
    skip = 1
    success = 2
    failure = 3
    downloading = 4

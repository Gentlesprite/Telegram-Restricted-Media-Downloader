# coding=UTF-8
# Author:LZY/我不是盘神
# Software:PyCharm
# Time:2024/1/2 17:43:02
# File:panel_form.py
from ctypes import windll
from prettytable import PrettyTable
from module import qrterm
from module.color_print import rainbow
from module.enum_define import StatusInfo
from module.color_print import print as print_with_color


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
    def __init__(self, title: str, header: tuple, data: list):
        self.table = PrettyTable(title=title, field_names=header)
        self.table.add_rows(data)

    def print_meta(self, color='Pink1'):
        print_with_color(self.table, color=color)


def pay():
    if check_run_env():  # 是终端才打印,生产环境会报错
        qrterm.draw('wxp://f2f0g8lKGhzEsr0rwtKWTTB2gQzs9Xg9g31aBvlpbILowMTa5SAMMEwn0JH1VEf2TGbS')
        rainbow('欢迎[微信扫码]支持作者!')


def check_run_env():  # 检测是控制台运行还是IDE运行
    return windll.kernel32.SetConsoleTextAttribute(windll.kernel32.GetStdHandle(-0xb), 0x7)

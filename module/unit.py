# coding=UTF-8
# Author:LZY/我不是盘神
# Software:PyCharm
# Time:2023/10/31 17:47:31
# File:unit.py
from typing import Tuple, List, Dict
import os
import mimetypes


def determine_suitable_units(number, unit=None):
    units = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
    if unit in units:
        index = units.index(unit)
        value = number / (1024 ** index)
        return float("{:.2f}".format(value)), unit
    else:
        values = [number]
        for i in range(len(units) - 1):
            if values[i] >= 1024:
                values.append(values[i] / 1024)
            else:
                break
        return "{:.2f}".format(values[-1]), units[len(values) - 1]


def suitable_units_display(number: int) -> str:
    return determine_suitable_units(number)[0] + determine_suitable_units(number)[1]


def read_media_type(file_path) -> Tuple[List[str], List[str], Dict[str, str]]:
    """判断并得到媒体类型文件名字列表
    参数
    ----------
    无
    原理:
        遍历文件目录下是媒体(图片,视频)的文件,
        将符合条件的追加到列表
    目的:
        去除非媒体文件名对程序运行的干扰
    返回
    -------
    元祖,传入路径目录下所有媒体(图片,视频)文件的名字,
        [0]目录下所有图片的名字列表:list[str]
        [1]视频下所有图片的名字列表:list[str]
        [2]对应关系字典:dict[str,[str]
    """
    image = []
    video = []
    file_type_info = {}
    for name in os.listdir(file_path):
        file_type, _ = mimetypes.guess_type(os.path.join(file_path, name))
        im_a_file = os.path.join(file_path, name)
        if os.path.isfile(im_a_file):
            try:
                file_main_type: str = file_type.split('/')[0]
                file_type_info[name] = file_main_type
            except AttributeError:
                pass  # 去掉NoneType的干扰
    for filename, file_type in file_type_info.items():
        if file_type == 'image':
            image.append(filename)
        if file_type == 'video':
            video.append(filename)
        elif file_type is None:
            continue
    return image, video, file_type_info

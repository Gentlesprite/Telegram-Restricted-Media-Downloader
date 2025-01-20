# coding=UTF-8
# Author:Gentlesprite
# Software:PyCharm
# Time:2023/11/13 20:34:13
# File:process_path.py
# 部分代码源于作者:tangyoha
import os
import re
import struct
import shutil
import datetime
import mimetypes
import unicodedata

from io import BytesIO
from pyrogram.file_id import (
    FILE_REFERENCE_FLAG,
    PHOTO_TYPES,
    WEB_LOCATION_FLAG,
    FileType,
    b64_decode,
    rle_decode,
)

from typing import Optional

from module.enum_define import Extension

_mimetypes = mimetypes.MimeTypes()


def split_path(path: str) -> dict:
    """将传入路径拆分为目录名和文件名并以字典形式返回。"""
    directory, file_name = os.path.split(path)
    return {'directory': directory, 'file_name': file_name}


def _is_directory_empty(directory_path: str) -> bool:
    """判断目录是否为空。"""
    if len(os.listdir(directory_path)) == 0:
        return True
    else:
        return False


def _is_exist(file_path: str) -> bool:
    """判断文件路径是否存在。"""
    return not os.path.isdir(file_path) and os.path.exists(file_path)


def _compare_file_size(local_size: int, sever_size: int) -> bool:
    """比较文件的大小是否一致。"""
    return local_size == sever_size


def is_file_duplicate(local_file_path: str, sever_size: int) -> bool:
    """判断文件是否重复。"""
    return _is_exist(local_file_path) and _compare_file_size(os.path.getsize(local_file_path), sever_size)


def validate_title(title: str) -> str:
    """验证并修改(如果不合法)标题的合法性。"""
    r_str = r"[/\\:*?\"<>|\n]"  # '/ \ : * ? " < > |'
    new_title = re.sub(r_str, "_", title)
    return new_title


def truncate_filename(path: str, limit: int = 230) -> str:
    # 作者:tangyoha
    """将文件名截断到最大长度。
    Parameters
    ----------
    path: str
        文件名路径

    limit: int
        文件名长度限制（以UTF-8 字节为单位）

    Returns
    -------
    str
        如果文件名的长度超过限制，则返回截断后的文件名；否则返回原始文件名。
    """
    p, f = os.path.split(os.path.normpath(path))
    f, e = os.path.splitext(f)
    f_max = limit - len(e.encode('utf-8'))
    f = unicodedata.normalize('NFC', f)
    f_trunc = f.encode()[:f_max].decode('utf-8', errors='ignore')
    return os.path.join(p, f_trunc + e)


def gen_backup_config(old_path: str, absolute_backup_dir: str, error_config: bool = False) -> str:
    """备份配置文件。"""
    os.makedirs(absolute_backup_dir, exist_ok=True)
    new_path = os.path.join(absolute_backup_dir,
                            f'{"error_" if error_config else ""}history_{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}_config.yaml')
    os.rename(old_path, new_path)
    return new_path


def safe_delete(file_path: str) -> bool:
    """删除文件或目录。"""
    try:
        if os.path.isdir(file_path):
            shutil.rmtree(file_path)
            return True
        elif os.path.isfile(file_path):
            os.remove(file_path)
            return True
    except FileNotFoundError:
        return True
    except PermissionError:
        return False
    except Exception as _:
        return False


def move_to_save_path(temp_save_path: str, save_path: str) -> dict:
    """移动文件到指定路径。"""
    try:
        os.makedirs(save_path, exist_ok=True)
        if os.path.isdir(save_path):
            shutil.move(temp_save_path, save_path)
            return {'e_code': None}
        else:
            if _is_directory_empty(save_path):
                os.rmdir(save_path)
            save_path = os.path.join(os.getcwd(), 'downloads')
            os.makedirs(save_path, exist_ok=True)
            shutil.move(temp_save_path, save_path)
            return {'e_code': f'"{save_path}"不是一个目录,已将文件下载到默认目录。'}
    except FileExistsError:
        return {'e_code': f'"{save_path}"已存在,不能重复保存。'}
    except Exception as e:
        return {'e_code': f'意外的错误,原因:"{e}"'}


def get_extension(file_id: str, mime_type: str, dot: bool = True) -> str:
    """获取文件的扩展名。
    更多扩展名见:http://www.iana.org/assignments/media-types/media-types.xhtml
    """

    if not file_id:
        if dot:
            return '.unknown'
        return 'unknown'

    file_type = _get_file_type(file_id)

    guessed_extension = _guess_extension(mime_type)

    if file_type in PHOTO_TYPES:
        extension = Extension.photo.get(mime_type, 'jpg')
    elif file_type == FileType.VOICE:
        extension = guessed_extension or 'ogg'
    elif file_type in (FileType.VIDEO, FileType.ANIMATION, FileType.VIDEO_NOTE):
        extension = guessed_extension or Extension.video.get(mime_type, 'mp4')
    elif file_type == FileType.DOCUMENT:
        if 'video' in mime_type:
            extension = guessed_extension or Extension.video.get(mime_type, 'mp4')
        elif 'image' in mime_type:
            extension = guessed_extension or Extension.photo.get(mime_type, 'jpg')  # v1.2.8 修复获取图片格式时,实际指向为视频字典的错误。
        else:
            extension = guessed_extension or 'zip'
    elif file_type == FileType.STICKER:
        extension = guessed_extension or 'webp'
    elif file_type == FileType.AUDIO:
        extension = guessed_extension or 'mp3'
    else:
        extension = 'unknown'

    if dot:
        extension = '.' + extension
    return extension


def _guess_extension(mime_type: str) -> Optional[str]:
    """如果扩展名不是None，则从没有点的MIME类型返回中猜测文件扩展名。"""
    extension = mimetypes.guess_extension(mime_type, strict=True)
    return extension[1:] if extension and extension.startswith('.') else extension


def _get_file_type(file_id: str):
    """获取文件类型。"""
    decoded = rle_decode(b64_decode(file_id))

    # File id versioning. Major versions lower than 4 don't have a minor version
    major = decoded[-1]

    if major < 4:
        buffer = BytesIO(decoded[:-1])
    else:
        buffer = BytesIO(decoded[:-2])

    file_type, _ = struct.unpack('<ii', buffer.read(8))

    file_type &= ~WEB_LOCATION_FLAG
    file_type &= ~FILE_REFERENCE_FLAG

    try:
        file_type = FileType(file_type)
    except ValueError as exc:
        raise ValueError(f'Unknown file_type {file_type} of file_id {file_id}') from exc

    return file_type

# coding=UTF-8
# Author:LZY/我不是盘神
# Software:PyCharm
# Time:2023/11/13 20:34:13
# File:process_path.py
import os
import re
import datetime
import unicodedata


def split_path(path):
    directory, file_name = os.path.split(path)
    return directory, file_name


def is_folder_empty(folder_path):
    if len(os.listdir(folder_path)) == 0:
        return True
    else:
        return False


def _is_exist(file_path: str) -> bool:
    return not os.path.isdir(file_path) and os.path.exists(file_path)


def _compare_file_size(local_size, sever_size) -> bool:
    return local_size == sever_size


def is_file_duplicate(local_file_path, sever_size):
    return _is_exist(local_file_path) and _compare_file_size(os.path.getsize(local_file_path), sever_size)


def validate_title(title: str) -> str:
    r_str = r"[/\\:*?\"<>|\n]"  # '/ \ : * ? " < > |'
    new_title = re.sub(r_str, "_", title)
    return new_title


def truncate_filename(path: str, limit: int = 230) -> str:
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
    f_max = limit - len(e.encode("utf-8"))
    f = unicodedata.normalize("NFC", f)
    f_trunc = f.encode()[:f_max].decode("utf-8", errors="ignore")
    return os.path.join(p, f_trunc + e)


def gen_backup_config(old_path: str, absolute_backup_dir: str, error_config: bool = False) -> str:
    os.makedirs(absolute_backup_dir, exist_ok=True)
    new_path = os.path.join(absolute_backup_dir,
                            f'{"error_" if error_config else ""}history_{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}_config.yaml')
    os.rename(old_path, new_path)
    return new_path

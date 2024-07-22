# coding=UTF-8
# Author:LZY/我不是盘神
# Software:PyCharm
# Time:2023/11/13 20:34:13
# File:process_path.py
import os
import re
import unicodedata


def split_path(path):
    directory, file_name = os.path.split(path)
    return directory, file_name


def is_folder_empty(folder_path):
    if len(os.listdir(folder_path)) == 0:
        return True
    else:
        return False


def is_exist(file_path: str) -> bool:
    """
    Check if a file exists and it is not a directory.

    Parameters
    ----------
    file_path: str
        Absolute path of the file to be checked.

    Returns
    -------
    bool
        True if the file exists else False.
    """
    return not os.path.isdir(file_path) and os.path.exists(file_path)



def validate_title(title: str) -> str:
    """Fix if title validation fails

    Parameters
    ----------
    title: str
        Chat title

    """
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
        文件名长度限制（以UTF-8字节为单位）

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

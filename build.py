# coding=UTF-8
# Author:Gentlesprite
# Software:PyCharm
# Time:2024/7/22 22:37
# File:build.py
import os
from module import AUTHOR, __version__, __update_date__, SOFTWARE_SHORT_NAME

ico_path = 'res/icon.ico'
output = 'output'
main = 'main.py'
years = __update_date__[:4]
include_module = '--include-module=pygments.lexers.data'
copy_right = f'Copyright (C) 2024-{years} {AUTHOR}.All rights reserved.'
build_command = f'nuitka --standalone --show-memory --show-progress --onefile {include_module} '
build_command += f'--output-dir={output} --file-version={__version__} '
build_command += f'--windows-icon-from-ico="{ico_path}" '
build_command += f'--output-filename="{SOFTWARE_SHORT_NAME}.exe" --copyright="{copy_right}"  --mingw64 '
build_command += f'--remove-output '
build_command += main
if __name__ == '__main__':
    try:
        print(build_command)
        os.system(build_command)
    except ImportError:
        print('请先使用命令:"pip install nuitka==2.4.8"安装Nuitka后重试。')

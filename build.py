# coding=UTF-8
# Author:Gentlesprite
# Software:PyCharm
# Time:2024/7/22 22:37
# File:build.py
"""pip install nuitka==2.4.8"""
import os
from module import author, __version__, __update_date__, SOFTWARE_FULL_NAME

app_name = SOFTWARE_FULL_NAME
file_version = __version__
ico_path = 'res/icon.ico'
output = 'output'
main = 'main.py'
years = __update_date__[:4]
include_module = '--include-module=pygments.lexers.data'
copy_right = f'Copyright (C) {years} {author}.'
build_command = f'nuitka --standalone --show-memory --show-progress --onefile {include_module} '
build_command += f'--output-dir={output} --file-version={file_version} '
build_command += f'--windows-icon-from-ico="{ico_path}" '
build_command += f'--output-filename="{app_name}.exe" --copyright="{copy_right}"  --mingw64 '
build_command += f'--remove-output '
build_command += main
if __name__ == '__main__':
    print(build_command)
    os.system(build_command)

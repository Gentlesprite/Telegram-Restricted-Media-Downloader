# coding=UTF-8
# Author:Gentlesprite
# Software:PyCharm
# Time:2024/7/22 22:37
# File:build
import os
from module import author, __version__,SOFTWARE_FULL_NAME
app_name = SOFTWARE_FULL_NAME
file_version = __version__
ico_path = 'doc/icon.ico'
output = 'output'
main = 'main.py'
copy_right = f'Copyright (C) 2024 {author}.'
build_command = f'nuitka --standalone --show-memory --show-progress --onefile '
build_command += f'--output-dir={output} --file-version={file_version} '
build_command += f'--windows-icon-from-ico="{ico_path}" '
build_command += f'--output-filename="{app_name}.exe" --copyright="{copy_right}"  --mingw64 '
build_command += main
print(build_command)
os.system(build_command)

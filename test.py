# coding=UTF-8
# Author:Gentlesprite
# Software:PyCharm
# Time:2024/7/2 2:39
# File:test
import os

temp_folder = r'D:\files\Documents\study\python\Program\Telegram_Restricted_Media_Downloader\temp'
temp_lst_dir: list = [os.path.join(temp_folder, i) for i in os.listdir(temp_folder)]
complete_media: list = [i for i in temp_lst_dir if not i.endswith('.temp')] if temp_lst_dir else []
for i in set(temp_lst_dir) ^ set(complete_media):
    print(i)

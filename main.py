# coding=UTF-8
# Author:LZY/我不是盘神
# Software:PyCharm
# Time:2023/11/18 12:31:18
# File:main.py
import os
from doc import qrterm
from pyrogram import Client
from module.app import Application
from module.enum_define import LogLevel
from module.logger_config import print_color
from limited_media_downloader import download_media_from_links
from module.logger_config import setup_no_console_loger_config, print_with_log


def pay():
    qrterm.draw('wxp://f2f0g8lKGhzEsr0rwtKWTTB2gQzs9Xg9g31aBvlpbILowMTa5SAMMEwn0JH1VEf2TGbS')
    print_color('欢迎[微信扫码]捐赠作者!', color='red')


if __name__ == '__main__':
    setup_no_console_loger_config()
    app = Application()
    app.config_leader()
    temp_folder = app.TEMP_FOLDER
    save_path = app.get_content('save_path')
    pay()
    try:
        os.makedirs(os.path.join(os.getcwd(), 'sessions'), exist_ok=True)
        client = Client(name='limited_downloader',
                        api_id=app.get_content('api_id'),
                        api_hash=app.get_content('api_hash'),
                        proxy=app.get_content('proxy') if app.get_content('proxy') else False,
                        workdir=os.path.join(os.getcwd(), 'sessions'))
        client.run(download_media_from_links(client=client,
                                             links=app.get_content('links'),
                                             max_download_task=app.get_content('max_download_task'),
                                             temp_folder=temp_folder,
                                             save_path=save_path))
    except KeyboardInterrupt:
        print_with_log(msg='用户手动终止下载任务。', level=LogLevel.info)
    finally:
        pay()
        os.system('pause')
        # todo 下载统计

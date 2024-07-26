# coding=UTF-8
# Author:LZY/我不是盘神
# Software:PyCharm
# Time:2023/11/18 12:31:18
# File:main.py
import os
from pyrogram import Client
from module.enum_define import LogLevel
from module.logger_config import setup_no_console_loger_config, print_with_log
from limited_media_downloader import download_media_from_links, _move_to_download_path

from module.app import Application

if __name__ == '__main__':
    setup_no_console_loger_config()
    app = Application()
    app.config_leader()
    temp_folder = app.TEMP_FOLDER
    save_path = app.get_content('save_path')
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
        # 如果用户主动中断,获取temp目录下已经下载好的文件,拼接成完整路径,移动到下载目录,避免下次重复下载
        # 先获取temp目录所有文件
        temp_lst_dir: list = [os.path.join(temp_folder, i) for i in os.listdir(temp_folder)]
        # 再获取非.temp文件
        complete_media: list = [i for i in temp_lst_dir if not i.endswith('.temp')] if temp_lst_dir else []
        # 找出两个列表不同的值为.temp
        temp_file = set(temp_lst_dir) ^ set(complete_media)
        # 删除temp文件
        if temp_file:
            for file in temp_file:
                try:
                    os.remove(file)
                    print_with_log(msg=f'成功删除缓存文件："{file}"。', level=LogLevel.success)
                except OSError as e:
                    print_with_log(msg=f'删除缓存文件"{file}"失败,原因:"{e}"请手动删除!', level=LogLevel.error)
        if complete_media:
            for temp_save_path in complete_media:
                try:
                    _move_to_download_path(temp_save_path, save_path)
                    print_with_log(
                        msg=f'下载完成的文件"{os.path.basename(temp_save_path)}"已移动到保存目录:"{save_path}"。',
                        level=LogLevel.success)
                except Exception as e:
                    print_with_log(
                        msg=f'移动下载完成的文件"{os.path.basename(temp_save_path)}"到保存目录失败,原因:"{e}"请前往"{temp_save_path}"手动移动!',
                        level=LogLevel.error)
        os.system('pause')
        # todo 下载统计

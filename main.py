# coding=UTF-8
# Author:LZY/我不是盘神
# Software:PyCharm
# Time:2023/11/18 12:31:18
# File:main.py
import os
import sys
import yaml
from pyrogram import Client
from limited_media_downloader import (download_media_from_links, _move_to_download_path, logger)

encoding = 'gbk'


def generate_config_content(content=None):
    config_file = {
        'api_hash': None,
        'api_id': None,
        'proxy': {'scheme': None,
                  'hostname': None,
                  'port': None,
                  'username': None,
                  'password': None},
        'links': '',
        'save_path': '',
        'max_download_task': 3,
    }
    dir_name = os.path.dirname(os.path.abspath(sys.argv[0]))  # 获取软件工作绝对目录
    config_name = 'config.yaml'  # 配置文件名
    config_path = os.path.join(dir_name, config_name)
    if not os.path.exists(config_path):
        with open(file=config_path, mode='w', encoding=encoding) as f:
            yaml.safe_dump(config_file, f)
    with open(file=config_path, mode='r', encoding=encoding) as f:
        config = yaml.safe_load(f)
    if content == 'proxy':
        basic_info = {}
        dlc_info = {}
        for key, value in config[content].items():
            if key == 'username' or key == 'password':
                dlc_info[key] = value
            else:
                basic_info[key] = value
        if all(dlc_info.values()):
            basic_info.update(dlc_info)
            return basic_info
        elif all(basic_info.values()):
            return basic_info
        else:
            return False

    else:
        if config.get(content):
            return config[content]
        else:
            new_value = input(f'请输入{content}:')
            config[content] = new_value

            with open(file=config_path, mode='r', encoding=encoding) as f:
                data = yaml.safe_load(f)

            data[content] = new_value

            with open(file=config_path, mode='w', encoding=encoding) as f:
                yaml.safe_dump(data, f)

            return config[content]


if __name__ == '__main__':
    temp_folder = os.path.join(os.getcwd(), 'temp')
    save_path = generate_config_content('save_path')
    try:
        os.makedirs(os.path.join(os.getcwd(), 'sessions'), exist_ok=True)
        client = Client(name='limited_downloader',
                        api_id=generate_config_content('api_id'),
                        api_hash=generate_config_content('api_hash'),
                        proxy=generate_config_content('proxy') if generate_config_content('proxy') else False,
                        workdir=os.path.join(os.getcwd(), 'sessions'))
        client.run(download_media_from_links(client=client,
                                             links=generate_config_content('links'),
                                             max_download_task=generate_config_content('max_download_task'),
                                             temp_folder=temp_folder,
                                             save_path=save_path))
    except KeyboardInterrupt:
        logger.info(f'用户手动终止下载任务。')
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
                    logger.success(f'成功删除缓存文件："{file}"。')
                except OSError as e:
                    logger.error(e)
        if complete_media:
            for temp_save_path in complete_media:
                try:
                    _move_to_download_path(temp_save_path, save_path)
                    logger.success(
                        f'下载完成的文件"{os.path.basename(temp_save_path)}"已移动到保存目录:"{save_path}"。')
                except Exception as e:
                    logger.error(e)

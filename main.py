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

DIR_NAME = os.path.dirname(os.path.abspath(sys.argv[0]))  # 获取软件工作绝对目录
CONFIG_NAME = 'config.yaml'  # 配置文件名
CONFIG_PATH = os.path.join(DIR_NAME, CONFIG_NAME)

CONFIG_TEMPLATE = {
    'api_hash': None,
    'api_id': None,
    'proxy': {
        'scheme': None,
        'hostname': None,
        'port': None,
        'username': None,
        'password': None
    },
    'links': '',
    'save_path': '',
    'max_download_task': 3,
}


def load_config(filename):
    try:
        if not os.path.exists(filename):
            return None
        with open(filename, 'r') as f:
            config = yaml.safe_load(f)
        return config
    except:
        print("检测到无效或缺失的配置文件。生成新的模板文件...")
        config = CONFIG_TEMPLATE.copy()
        return config


def save_config(config, filename):
    with open(filename, 'w') as f:
        yaml.dump(config, f)


def is_config_valid(config):
    # Check if all required keys exist in the config dictionary
    required_keys = ['api_hash', 'api_id', 'proxy', 'links', 'save_path', 'max_download_task']
    for key in required_keys:
        if key not in config:
            return False
    return True


def prompt_for_proxy_config(config):
    proxy_config = config['proxy']
    proxy_config['scheme'] = input('请输入代理类型 (http/socks5): ')
    proxy_config['hostname'] = input('请输入代理IP地址: ')
    proxy_config['port'] = int(input('请输入代理端口: '))
    if input('代理是否需要认证? (y/n)').lower() == 'y':
        proxy_config['username'] = input('请输入用户名: ')
        proxy_config['password'] = input('请输入密码: ')


def config_leader():
    # Load the existing config file or use default config
    config = load_config(CONFIG_PATH)

    # Prompt user to input necessary configurations
    config['api_hash'] = input('请输入api_hash: ')
    config['api_id'] = input('请输入api_id: ')
    config['links'] = input('请输入链接: ')
    config['save_path'] = input('请输入保存路径: ')
    config['max_download_task'] = int(input('请输入最大下载任务数: '))

    # Prompt for proxy configuration if needed
    if input('是否需要使用代理? (y/n)').lower() == 'y':
        config['proxy'] = {}
        prompt_for_proxy_config(config)

    # Save the updated config
    save_config(config, CONFIG_PATH)
    print('配置文件更新成功。')
    return


def get_content(content):
    with open(CONFIG_PATH, 'r', encoding='UTF-8') as f:
        data = yaml.safe_load(f)
    return data.get(content)


if __name__ == '__main__':
    config_leader()
    temp_folder = os.path.join(os.getcwd(), 'temp')
    save_path = get_content('save_path')
    try:
        os.makedirs(os.path.join(os.getcwd(), 'sessions'), exist_ok=True)
        client = Client(name='limited_downloader',
                        api_id=get_content('api_id'),
                        api_hash=get_content('api_hash'),
                        proxy=get_content('proxy') if get_content('proxy') else False,
                        workdir=os.path.join(os.getcwd(), 'sessions'))
        client.run(download_media_from_links(client=client,
                                             links=get_content('links'),
                                             max_download_task=get_content('max_download_task'),
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

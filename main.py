# coding=UTF-8
# Author:LZY/我不是盘神
# Software:PyCharm
# Time:2023/11/18 12:31:18
# File:main.py
import os
import sys
import yaml
from pyrogram import Client
from module.enum_define import LogLevel
from module.logger_config import setup_no_console_loger_config, print_with_log
from limited_media_downloader import download_media_from_links, _move_to_download_path

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


def load_config(config_path):
    try:
        if not os.path.exists(config_path):
            with open(file=config_path, mode='w') as f:
                yaml.safe_dump(CONFIG_TEMPLATE, f)
            print_with_log(msg='未找到配置文件，已生成新的模板文件...', level=LogLevel.info)
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
            if config is None:
                print_with_log(msg='检测到空的配置文件。已生成新的模板文件...', level=LogLevel.warning)
                return CONFIG_TEMPLATE.copy()
        return config
    except:
        print_with_log(msg='检测到无效或损坏的配置文件。已生成新的模板文件...', level=LogLevel.warning)
        # todo 不是删除文件而是更名文件
        os.remove(config_path, config_path + 'old_backup')
        config = CONFIG_TEMPLATE.copy()
        return config


def save_config(config, filename):
    with open(filename, 'w') as f:
        yaml.dump(config, f)


def config_leader():
    # Load the existing config file or use default config
    config = load_config(CONFIG_PATH)
    # Prompt user to input necessary configurations
    if not config['api_hash']:
        config['api_hash'] = input('请输入api_hash:')
    if not config['api_id']:
        config['api_id'] = str(input('请输入api_id:'))
    if not config['links']:
        # 输入需要下载的媒体链接文件路径，确保文件存在
        while True:
            links_file = None
            try:
                links_file = input('请输入需要下载的媒体链接 [.txt] 格式的路径:').strip()
                if os.path.isfile(links_file):
                    config['links'] = links_file
                    break
                elif not os.path.normpath(links_file).endswith('.txt'):
                    print_with_log(msg=f'意外的参数:"{links_file}"文件路径必须以[.txt]结尾，请重新输入!',
                                   level=LogLevel.warning)
                else:
                    print_with_log(msg=f'意外的参数:"{links_file}"文件路径必须以[.txt]结尾，请重新输入!',
                                   level=LogLevel.warning)
            except:
                print_with_log(msg=f'意外的参数:"{links_file}"接受到了意外的输入,请重新输入!',
                               level=LogLevel.error.text)
    if not config['save_path']:
        # 输入媒体保存路径，确保是一个有效的目录路径
        while True:
            save_path = input('请输入媒体保存路径:').strip()
            if os.path.isdir(save_path):
                config['save_path'] = save_path
                break
            else:
                print_with_log(f'意外的参数:"{save_path}"指定的路径无效或不是一个目录,请重新输入!',
                               level=LogLevel.warning.text)
    if not config['max_download_task']:
        # 输入最大下载任务数，确保是一个整数且不超过特定限制
        while True:
            max_tasks = None
            try:
                max_tasks = int(
                    input('请输入最大下载任务数 [默认为3] 非会员不建议大于5，容易被限制为强制单任务下载:').strip())
                if max_tasks <= 0:
                    print_with_log(msg=f'意外的参数:"{max_tasks}"任务数必须是正整数，请重新输入!',
                                   level=LogLevel.warning)
                else:
                    config['max_download_task'] = max_tasks
                    break
            except ValueError:
                print_with_log(msg=f'意外的参数:"{max_tasks}"请输入一个有效的整数作为最大下载任务数!',
                               level=LogLevel.error)
    proxy_main_info: list = ['scheme', 'hostname', 'port']  # 代理的主要信息来判断是否需要使用代理
    is_none = []
    for i in proxy_main_info:
        is_none.append(config.get('proxy')[i])
    if not all(is_none):
        # Prompt for proxy configuration if needed
        if input('是否需要使用代理? [y|n]').lower() == 'y':
            config['proxy'] = {}
            proxy_config = config['proxy']
            # 输入代理类型
            while True:
                scheme = input('请输入代理类型[http|socks5]:').strip().lower()
                if scheme in ['http', 'socks5']:
                    proxy_config['scheme'] = scheme
                    break
                else:
                    print_with_log(msg='请输入有效的代理类型!', level=LogLevel.warning)
            # 输入代理IP地址
            proxy_config['hostname'] = input('请输入代理IP地址:').strip()
            # 输入代理端口
            while True:
                port = None
                try:
                    port = int(input('请输入代理端口:').strip())
                    if port > 0 and port <= 65535:
                        proxy_config['port'] = port
                        break
                    else:
                        print_with_log(msg=f'"{port}"端口号必须在1到65535之间!', level=LogLevel.warning)
                except ValueError:
                    print_with_log(msg=f'"{port}"请输入一个有效的整数作为端口号!', level=LogLevel.warning)
            # 是否需要认证
            if input('代理是否需要认证?[y|n]').strip().lower() == 'y':
                proxy_config['username'] = input('请输入用户名:').strip()
                proxy_config['password'] = input('请输入密码:').strip()

    # Save the updated config
    save_config(config, CONFIG_PATH)
    print_with_log(msg=f'"{config}"配置文件更新成功。', level=LogLevel.success)
    return


def get_content(content):
    with open(CONFIG_PATH, 'r', encoding='UTF-8') as f:
        data = yaml.safe_load(f)
    return data.get(content)


if __name__ == '__main__':
    setup_no_console_loger_config()
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

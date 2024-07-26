# coding=UTF-8
# Author:Gentlesprite
# Software:PyCharm
# Time:2024/7/25 12:32
# File:app
import os
import sys
import yaml
import datetime
from module.logger_config import print_with_log
from module.enum_define import LogLevel
from module.panel_form import PanelTable


class Application:
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
    TEMP_FOLDER = os.path.join(os.getcwd(), 'temp')

    def __init__(self):
        self.config_path = Application.CONFIG_PATH
        self.config = self.load_config()

    def get_content(self, content):
        with open(self.config_path, 'r', encoding='UTF-8') as f:
            data = yaml.safe_load(f)
        return data.get(content)

    def load_config(self):
        try:
            if not os.path.exists(self.config_path):
                with open(file=self.config_path, mode='w') as f:
                    yaml.safe_dump(Application.CONFIG_TEMPLATE, f)
                print_with_log(msg='未找到配置文件，已生成新的模板文件...', level=LogLevel.info)
            with open(self.config_path, 'r') as f:
                config = yaml.safe_load(f)
                if config is None:
                    print_with_log(msg='检测到空的配置文件。已生成新的模板文件...', level=LogLevel.warning)
                    return Application.CONFIG_TEMPLATE.copy()
            return config
        except Exception as e:
            print_with_log(msg=f'检测到无效或损坏的配置文件。已生成新的模板文件...原因:"{e}"', level=LogLevel.warning)
            os.rename(self.config_path,
                      os.path.join(Application.DIR_NAME,
                                   f'history_{datetime.datetime.now().strftime("%H-%M-%S")}_config.yaml'))
            config = Application.CONFIG_TEMPLATE.copy()
            return config

    def save_config(self):
        with open(self.config_path, 'w') as f:
            yaml.dump(self.config, f)

    def config_leader(self):
        # Prompt user to input necessary configurations
        if not self.config['api_hash']:
            self.config['api_hash'] = input('请输入api_hash:')
        if not self.config['api_id']:
            self.config['api_id'] = str(input('请输入api_id:'))
        if not self.config['links']:
            # 输入需要下载的媒体链接文件路径，确保文件存在
            while True:
                links_file = None
                try:
                    links_file = input('请输入需要下载的媒体链接 [.txt] 格式的路径:').strip()
                    if os.path.isfile(links_file):
                        self.config['links'] = links_file
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
        if not self.config['save_path']:
            # 输入媒体保存路径，确保是一个有效的目录路径
            while True:
                save_path = input('请输入媒体保存路径:').strip()
                if os.path.isdir(save_path):
                    self.config['save_path'] = save_path
                    break
                else:
                    print_with_log(f'意外的参数:"{save_path}"指定的路径无效或不是一个目录,请重新输入!',
                                   level=LogLevel.warning.text)
        if not self.config['max_download_task']:
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
                        self.config['max_download_task'] = max_tasks
                        break
                except ValueError:
                    print_with_log(msg=f'意外的参数:"{max_tasks}"请输入一个有效的整数作为最大下载任务数!',
                                   level=LogLevel.error)
        proxy_main_info: list = ['scheme', 'hostname', 'port']  # 代理的主要信息来判断是否需要使用代理
        is_none = []
        for i in proxy_main_info:
            is_none.append(self.config.get('proxy')[i])
        if not all(is_none):
            # Prompt for proxy configuration if needed
            if input('是否需要使用代理? [y|n]').lower() == 'y':
                self.config['proxy'] = {}
                proxy_config = self.config['proxy']
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
        self.save_config()
        header = []
        data = []
        for i in self.config.items():
            header.append(i[0])
            data.append(i[1])

        pt = PanelTable('配置信息', header, data)
        pt.print_meta()
        return

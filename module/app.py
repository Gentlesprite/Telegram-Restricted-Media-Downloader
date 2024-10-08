# coding=UTF-8
# Author:Gentlesprite
# Software:PyCharm
# Time:2024/7/25 12:32
# File:app
import os
import sys
import yaml
import ipaddress
from loguru import logger
from module.process_path import gen_backup_config


class Application:
    DIR_NAME = os.path.dirname(os.path.abspath(sys.argv[0]))  # 获取软件工作绝对目录
    CONFIG_NAME = 'config.yaml'  # 配置文件名
    CONFIG_PATH = os.path.join(DIR_NAME, CONFIG_NAME)
    CONFIG_TEMPLATE = {
        'api_id': None,
        'api_hash': None,
        'proxy': {
            'enable_proxy': None,
            'is_notice': None,
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
        self.input_link = []

    def load_config(self):
        config = Application.CONFIG_TEMPLATE.copy()
        try:
            if not os.path.exists(self.config_path):
                with open(file=self.config_path, mode='w', encoding='UTF-8') as f:
                    yaml.safe_dump(Application.CONFIG_TEMPLATE, f)
                logger.info('未找到配置文件,已生成新的模板文件...')
            with open(self.config_path, 'r') as f:
                config = yaml.safe_load(f)
        except UnicodeDecodeError as e:  # v1.1.3加入配置文件路径是中文或特殊字符时的错误提示,由于nuitka打包的性质决定,
            # 中文路径无法被打包好的二进制文件识别,故在配置文件时无论是链接路径还是媒体保存路径都请使用英文命名。
            logger.warning(
                f'读取配置文件遇到编码错误,可能保存路径中包含中文或特殊字符的文件夹。已生成新的模板文件...原因:"{e}"')
            backup_path = gen_backup_config(old_path=self.config_path, dir_name=Application.DIR_NAME)
            logger.success(f'原来的配置文件已备份至"{backup_path}"')
        except Exception as e:
            logger.warning('注意链接路径和保存路径不能有引号!')
            logger.warning(f'检测到无效或损坏的配置文件。已生成新的模板文件...原因:"{e}"')
            backup_path = gen_backup_config(old_path=self.config_path, dir_name=Application.DIR_NAME)
            logger.success(f'原来的配置文件已备份至"{backup_path}"')
        finally:
            if config is None:
                logger.warning('检测到空的配置文件。已生成新的模板文件...')
                config = Application.CONFIG_TEMPLATE.copy()
            return config

    def save_config(self):
        with open(self.config_path, 'w') as f:
            yaml.dump(self.config, f)

    def config_guide(self):
        # input user to input necessary configurations
        # v1.1.0 更替api_id和api_hash位置,与telegram申请的api位置对应以免输错
        record_flag = False

        def check_proxy_params(config: dict):
            for i in Application.CONFIG_TEMPLATE.items():  # 添加与模板没有的字段
                if i[0] == 'proxy':
                    for j in i[1].items():
                        if j[0] not in config:
                            logger.info(f'"{j[0]}"不在proxy字段中,已添加。')
                            config[j[0]] = j[1]

        def is_proxy_input(config: dict):  # 检测代理配置是否需要用户输入
            result = False
            basic_truth_table: list = []
            advance_account_truth_table: list = []
            if config.get('enable_proxy') is False:  # 检测打开了代理但是代理配置错误
                return False
            for _ in config.items():
                if _[0] in ['scheme', 'port', 'hostname']:
                    basic_truth_table.append(_[1])
                if _[0] in ['username', 'password']:
                    advance_account_truth_table.append(_[1])
            if all(basic_truth_table) is False:
                logger.info('请配置代理!')
                result = True
            if any(advance_account_truth_table) and all(advance_account_truth_table) is False:
                logger.warning('代理账号或密码未输入!')
                result = True
            return result

        def keyboard_interrupt():  # 用户键盘中断
            new_line = True
            try:
                if record_flag:
                    print('\n')
                    while True:
                        is_save = input('[退出提示]是否需要保存当前已填写的参数? - [y|n]:').lower()
                        if is_save == 'y':
                            logger.success('配置已保存!')
                            self.save_config()
                            break
                        elif is_save == 'n':
                            logger.info('不保存当前填写参数。')
                            break
                else:
                    exit()
            except KeyboardInterrupt:
                new_line = False
                print('\n')
                logger.info('用户放弃保存,手动终止配置参数。')
            finally:
                if new_line is True:
                    print('\n')
                    logger.info('用户手动终止配置参数。')
                os.system('pause')
                exit()

        if not self.config['api_id']:
            valid_length: int = 8
            while True:
                try:
                    api_id = str(input('请输入api_id:'))
                    if len(api_id) == valid_length and api_id.isdigit():
                        self.config['api_id'] = api_id
                        record_flag = True
                        break
                    else:
                        logger.warning(f'意外的参数:"{api_id}",不是一个[{valid_length}位]的纯数字!请重新输入!')
                except KeyboardInterrupt:
                    keyboard_interrupt()
        if not self.config['api_hash']:
            valid_length: int = 32
            while True:
                try:
                    api_hash = input('请输入api_hash:')
                    if len(api_hash) == 32:
                        self.config['api_hash'] = api_hash
                        record_flag = True
                        break
                    else:
                        logger.warning(f'"{api_hash}"不是一个[{valid_length}位]的纯数字!请重新输入!')
                except KeyboardInterrupt:
                    keyboard_interrupt()
        if not self.config['links']:
            # 输入需要下载的媒体链接文件路径,确保文件存在
            valid_format = "[.txt]"
            links_file = None
            while True:
                try:
                    links_file = input(f'请输入需要下载的媒体链接的[完整路径],格式 - {valid_format}:').strip()
                    if os.path.isfile(links_file):
                        self.config['links'] = links_file
                        record_flag = True
                        break
                    elif not os.path.normpath(links_file).endswith('.txt'):
                        logger.warning(f'意外的参数:"{links_file}",文件路径必须以[.txt]结尾,请重新输入!')
                    else:
                        logger.warning(f'意外的参数:"{links_file}",文件路径必须以[.txt]结尾,并且必须存在,请重新输入!')
                except KeyboardInterrupt:
                    keyboard_interrupt()
                except Exception as e:
                    logger.error(f'"{e}"意外的参数:"{links_file}",请重新输入!')
        if not self.config['save_path']:
            # 输入媒体保存路径,确保是一个有效的目录路径
            while True:
                try:
                    save_path = input('请输入媒体保存路径:').strip()
                    if os.path.isdir(save_path):
                        self.config['save_path'] = save_path
                        record_flag = True
                        break
                    elif os.path.isfile(save_path):
                        logger.warning(f'意外的参数:"{save_path}",指定的路径是一个文件并非目录,请重新输入!')
                    else:
                        logger.warning(f'意外的参数:"{save_path}",指定的路径无效或不是一个目录,请重新输入!')
                except KeyboardInterrupt:
                    keyboard_interrupt()
        if not self.config['max_download_task']:
            # 输入最大下载任务数,确保是一个整数且不超过特定限制
            max_tasks = None
            while True:
                try:
                    max_tasks = int(
                        input('请输入最大下载任务数[默认为3]非会员不建议大于[5],容易被限制为强制单任务下载:').strip())
                    if max_tasks <= 0:
                        logger.warning(f'意外的参数:"{max_tasks}"任务数必须是[正整数],请重新输入!')
                    else:
                        self.config['max_download_task'] = max_tasks
                        record_flag = True
                        break
                except ValueError:
                    logger.error(f'意外的参数:"{max_tasks}",请输入一个有效的[正整数]作为最大下载任务数!')
                except KeyboardInterrupt:
                    keyboard_interrupt()
        proxy_config: dict = self.config.get('proxy')  # 读取proxy字段得到字典
        check_proxy_params(proxy_config)  # 检查代理字典字段是否完整并自动补全保存

        enable_proxy = self.config.get('proxy', {}).get('enable_proxy')
        if proxy_config.get('is_notice') is True or proxy_config.get('is_notice') is None:  # 如果打开了通知或第一次配置
            try:
                while True:
                    enable_proxy = input('是否需要使用代理? - [y|n]:').lower()  # 询问是否开启代理
                    if enable_proxy == 'y':
                        break
                    elif enable_proxy == 'n':
                        break
                while True:
                    remember_choice = input('下次是否不再询问使用代理? - [y|n]:').lower()  # 是否记住选项
                    if remember_choice == 'y':
                        proxy_config['is_notice'] = False
                        record_flag = True
                        logger.info('已设置为下次不再询问是否使用代理!')
                        break
                    elif remember_choice == 'n':
                        proxy_config['is_notice'] = True
                        record_flag = True
                        logger.info('已设置为下次仍然询问是否使用代理!')
                        break
            except KeyboardInterrupt:
                keyboard_interrupt()

        if enable_proxy == 'y' or enable_proxy is True:
            proxy_config['enable_proxy'] = True
            if is_proxy_input(proxy_config):
                valid_ip = 'x.x.x.x'
                valid_port = '0~65535'
                ip_address = ''
                port = -1
                valid_scheme: list = ['http', 'socks4', 'socks5']
                # 输入代理类型
                if not proxy_config['scheme']:
                    while True:
                        try:
                            scheme = input(f'请输入代理类型 - [{"|".join(valid_scheme)}]:').strip().lower()
                            if scheme in valid_scheme:
                                proxy_config['scheme'] = scheme
                                record_flag = True
                                break
                            else:
                                logger.warning(
                                    f'意外的参数:"{scheme}",请输入有效的代理类型 - [{"|".join(valid_scheme)}]!')
                        except KeyboardInterrupt:
                            keyboard_interrupt()
                if not proxy_config['hostname']:
                    while True:
                        # 输入代理IP地址
                        try:
                            ip_address = input(f'请输入{scheme}代理的IP地址 - [{valid_ip}]:').strip()
                            if isinstance(ipaddress.ip_address(ip_address), ipaddress.IPv4Address):
                                proxy_config['hostname'] = ip_address
                                record_flag = True
                                break
                        except ValueError:
                            logger.warning(f'"{ip_address}"不是一个ip地址,请输入有效的ipv4地址 - [{valid_ip}]!')
                        except KeyboardInterrupt:
                            keyboard_interrupt()
                if not proxy_config['port']:
                    # 输入代理端口
                    while True:
                        try:
                            port = int(input(f'请输入代理端口 - [{valid_port}]:').strip())
                            if 0 < port <= 65535:
                                proxy_config['port'] = port
                                record_flag = True
                                break
                            else:
                                logger.warning(f'意外的参数:"{port}",端口号必须在1到65535之间!')
                        except ValueError:
                            logger.warning(f'意外的参数:"{port}",请输入一个有效的整数 - [{valid_port}]!')
                        except KeyboardInterrupt:
                            keyboard_interrupt()
                if not all([proxy_config['username'], proxy_config['password']]):
                    # 是否需要认证
                    while True:
                        if input('代理是否需要认证?[y|n]:').strip().lower() == 'y':
                            try:
                                proxy_config['username'] = input('请输入用户名:').strip()
                                record_flag = True
                                proxy_config['password'] = input('请输入密码:').strip()
                                record_flag = True
                            except KeyboardInterrupt:
                                keyboard_interrupt()
                            finally:
                                break
                        elif input('代理是否需要认证?[y|n]:').strip().lower() == 'n':
                            if any([proxy_config['username'], proxy_config['password']]):
                                proxy_config['username'] = None
                                proxy_config['password'] = None
                                break

        self.save_config()
        return

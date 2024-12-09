# coding=UTF-8
# Author:Gentlesprite
# Software:PyCharm
# Time:2024/7/25 12:32
# File:app
import time
import subprocess
import ipaddress
from rich.table import Table
from rich.markdown import Markdown
from module import os
from module import sys
from module import datetime
from module import qrterm
from module import check_run_env
from module import logger
from module import console
from module import yaml
from module import CustomDumper
from module import SOFTWARE_FULL_NAME, __version__, __copyright__, __license__
from module.process_path import gen_backup_config
from module.enum_define import GradientColor, ArtFont


class Validator:
    @staticmethod
    def is_valid_api_id(api_id: str, valid_length: int = 32) -> bool:
        try:
            if len(api_id) < valid_length:
                if api_id.isdigit():
                    return True
                else:
                    logger.warning(f'意外的参数:"{api_id}",不是「纯数字」请重新输入!')
                    return False
            else:
                logger.warning(f'意外的参数,填写的"{api_id}"可能是「api_hash」,请填入正确的「api_id」!')
                return False
        except (AttributeError, TypeError):
            logger.error('手动编辑config.yaml时,api_id需要有引号!')
            return False

    @staticmethod
    def is_valid_api_hash(api_hash: str, valid_length: int = 32) -> bool:
        return len(str(api_hash)) == valid_length

    @staticmethod
    def is_valid_links_file(file_path: str, valid_format: str = '.txt') -> bool:
        file_path = os.path.normpath(file_path)
        return os.path.isfile(file_path) and file_path.endswith(valid_format)

    @staticmethod
    def is_valid_save_path(save_path: str) -> bool:
        if not os.path.exists(save_path):
            while True:
                try:
                    question = console.input(f'目录:"{save_path}"不存在,是否创建? - 「y|n」(默认y):')
                    if question == 'y' or question == '':
                        os.makedirs(save_path, exist_ok=True)
                        logger.success(f'成功创建目录:"{save_path}"')
                        break
                    elif question == 'n':
                        break
                    else:
                        logger.warning(f'意外的参数:"{question}",支持的参数 - 「y|n」')
                except Exception as e:
                    logger.error(f'意外的错误,原因:"{e}"')
                    break
        return os.path.isdir(save_path)

    @staticmethod
    def is_valid_max_download_task(max_tasks: int) -> bool:
        try:
            return int(max_tasks) > 0
        except ValueError:
            return False
        except Exception as e:
            logger.error(f'意外的错误,原因:"{e}"')

    @staticmethod
    def is_valid_enable_proxy(enable_proxy: str or bool) -> bool:
        if enable_proxy == 'y' or enable_proxy == 'n':
            return True

    @staticmethod
    def is_valid_is_notice(is_notice: str) -> bool:
        if is_notice == 'y' or is_notice == 'n':
            return True

    @staticmethod
    def is_valid_scheme(scheme: str, valid_format: list) -> bool:
        return scheme in valid_format

    @staticmethod
    def is_valid_hostname(hostname: str) -> bool:
        return isinstance(ipaddress.ip_address(hostname), ipaddress.IPv4Address)

    @staticmethod
    def is_valid_port(port: int) -> bool:
        try:
            return 0 < int(port) <= 65535
        except ValueError:  # 处理非整数字符串的情况
            return False
        except TypeError:  # 处理传入非数字类型的情况
            return False
        except Exception as e:
            logger.error(f'意外的错误,原因:"{e}"')
            return False


class Application:
    # 将 None 的表示注册到 Dumper 中

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
        'links': None,
        'save_path': None,
        'max_download_task': None,
        'is_shutdown': None
    }
    TEMP_FOLDER = os.path.join(os.getcwd(), 'temp')
    BACKUP_DIR = 'ConfigBackup'
    ABSOLUTE_BACKUP_DIR = os.path.join(DIR_NAME, BACKUP_DIR)

    def __init__(self):
        self.color: list = GradientColor.blue_to_purple
        self.history_timestamp: dict = {}
        self.input_link: list = []
        self.last_record: dict = {}
        self.difference_timestamp: dict = {}
        self.config_path: str = Application.CONFIG_PATH
        self.record_flag: bool = False
        self.modified = False
        self.history_record()
        self.config = self.load_config()

    @staticmethod
    def shutdown_task(second: int):
        try:
            # 启动关机命令
            shutdown_command = f'shutdown -s -t {second}'
            subprocess.Popen(shutdown_command, shell=True)  # 异步执行关机
            # 实时显示倒计时
            for remaining in range(second, 0, -1):
                console.print(f'即将在{remaining}秒后关机, 按「CTRL+C」可取消。', end='\r', style='#ff4805')
                time.sleep(1)
            console.print('\n关机即将执行!', style='#f6ad00')
        except KeyboardInterrupt:
            subprocess.Popen('shutdown -a', shell=True)
            console.print('\n关机已被用户取消!', style='#19ac18')
            os.system('pause')

    def backup_config(self, backup_config: str, error_config: bool = False):
        if backup_config != Application.ABSOLUTE_BACKUP_DIR:
            backup_path = gen_backup_config(old_path=self.config_path,
                                            absolute_backup_dir=Application.ABSOLUTE_BACKUP_DIR,
                                            error_config=error_config)
            logger.success(f'原来的配置文件已备份至"{backup_path}"')
        else:
            logger.success('配置文件与模板文件完全一致,无需备份。')

    def load_config(self, error_config: bool = False) -> dict:
        config = Application.CONFIG_TEMPLATE.copy()
        try:
            if not os.path.exists(self.config_path):
                with open(file=self.config_path, mode='w', encoding='UTF-8') as f:
                    yaml.dump(Application.CONFIG_TEMPLATE, f, Dumper=CustomDumper)
                logger.info('未找到配置文件,已生成新的模板文件...')
            with open(self.config_path, 'r') as f:
                config = yaml.safe_load(f)  # v1.1.4加入对每个字段的完整性检测
            config = self._check_params(config)  # 检查所有字段是否完整,modified代表是否有修改记录(只记录缺少的)
        except UnicodeDecodeError as e:  # v1.1.3加入配置文件路径是中文或特殊字符时的错误提示,由于nuitka打包的性质决定,
            # 中文路径无法被打包好的二进制文件识别,故在配置文件时无论是链接路径还是媒体保存路径都请使用英文命名。
            error_config: bool = True
            logger.warning(
                f'读取配置文件遇到编码错误,可能保存路径中包含中文或特殊字符的文件夹。已生成新的模板文件...原因:"{e}"')
            self.backup_config(config, error_config=error_config)
        except Exception as e:
            error_config: bool = True
            console.print('「注意」链接路径和保存路径不能有引号!', style='red')
            logger.warning(f'检测到无效或损坏的配置文件。已生成新的模板文件...原因:"{e}"')
            self.backup_config(config, error_config=error_config)
        finally:
            if config is None:
                logger.warning('检测到空的配置文件。已生成新的模板文件...')
                config = Application.CONFIG_TEMPLATE.copy()
            if error_config:  # 如果遇到报错或者全部参数都是空的
                return config
            elif not self.modified and config != Application.CONFIG_TEMPLATE:  # v1.1.4 加入是否重新编辑配置文件的引导。保证配置文件没有缺少任何字段,否则不询问
                while True:
                    try:
                        question = console.input(
                            '检测到已配置完成的配置文件,是否需要重新配置?(之前的配置文件将为你备份到当前目录下) - 「y|n」(默认n):').lower()
                        if question == 'y':
                            config = Application.CONFIG_TEMPLATE.copy()
                            backup_path = gen_backup_config(old_path=self.config_path,
                                                            absolute_backup_dir=Application.ABSOLUTE_BACKUP_DIR)
                            logger.success(
                                f'原来的配置文件已备份至"{backup_path}"')
                            self.history_record()  # 更新到上次填写的记录
                            break
                        elif question == 'n' or question == '':
                            break
                        else:
                            logger.warning(f'意外的参数:"{question}",支持的参数 - 「y|n」(默认n)')
                    except KeyboardInterrupt:
                        self._keyboard_interrupt()
            return config

    def save_config(self):
        with open(self.config_path, 'w') as f:
            yaml.dump(self.config, f)

    def _check_params(self, config: dict, history=False):
        # 如果 config 为 None，初始化为一个空字典
        if config is None:
            config = {}

        def add_missing_keys(target, template, log_message):
            # 添加缺失的字段并记录日志
            for key, value in template.items():
                if key not in target:
                    target[key] = value
                    if not history:
                        logger.info(log_message.format(key))
                        self.modified = True
                        self.record_flag = True

        def remove_extra_keys(target, template, log_message):
            # 删除多余的字段并记录日志
            keys_to_remove = [key for key in target.keys() if key not in template]
            for key in keys_to_remove:
                target.pop(key)
                if not history:
                    logger.info(log_message.format(key))
                    self.record_flag = True

        # 处理父级字段
        add_missing_keys(target=config, template=Application.CONFIG_TEMPLATE, log_message='"{}"不在配置文件中,已添加。')
        # 特殊处理 proxy 字段
        if 'proxy' in config:
            proxy_template = Application.CONFIG_TEMPLATE['proxy']
            proxy_config = config['proxy']

            # 确保 proxy_config 是字典
            if not isinstance(proxy_config, dict):
                proxy_config = {}
                config['proxy'] = proxy_config

            add_missing_keys(proxy_config, proxy_template, '"{}"不在proxy配置中,已添加。')
            remove_extra_keys(proxy_config, proxy_template, '"{}"不在proxy模板中,已删除。')

        # 删除父级模板中没有的字段
        remove_extra_keys(config, Application.CONFIG_TEMPLATE, '"{}"不在模板中,已删除。')

        return config

    def _is_proxy_input(self, config: dict):  # 检测代理配置是否需要用户输入
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
            console.print('请配置代理!', style=self.color[8])
            result = True
        if any(advance_account_truth_table) and all(advance_account_truth_table) is False:
            logger.warning('代理账号或密码未输入!')
            result = True
        return result

    def _keyboard_interrupt(self):  # 用户键盘中断
        new_line = True
        try:
            if self.record_flag:
                print('\n')
                while True:
                    question = console.input('「退出提示」是否需要保存当前已填写的参数? - 「y|n」:').lower()
                    if question == 'y':
                        logger.success('配置已保存!')
                        self.save_config()
                        break
                    elif question == 'n':
                        logger.info('不保存当前填写参数。')
                        break
                    else:
                        logger.warning(f'意外的参数:"{question}",支持的参数 - 「y|n」')
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

    def _find_history_config(self):
        if not self.history_timestamp:
            return {}
        if not self.difference_timestamp:
            return {}
        try:
            min_key = min(self.difference_timestamp.keys())
            min_diff_timestamp = self.difference_timestamp.get(min_key)
            min_config_file = self.history_timestamp.get(min_diff_timestamp)
            if not min_config_file:
                return {}
            last_config_file = os.path.join(Application.ABSOLUTE_BACKUP_DIR, min_config_file)  # 拼接文件路径
            with open(file=last_config_file, mode='r', encoding='UTF-8') as f:
                config = yaml.safe_load(f)
            last_record = self._check_params(config, history=True)  # v1.1.6修复读取历史如果缺失字段使得flag置True

            if last_record == Application.CONFIG_TEMPLATE:
                # 从字典中删除当前文件
                self.history_timestamp.pop(min_diff_timestamp, None)
                self.difference_timestamp.pop(min_key, None)
                # 递归调用
                return self._find_history_config()
            else:
                return last_record
        except Exception as e:
            logger.error(e)
            return {}

    def history_record(self):

        # 首先判断是否存在目录文件
        try:
            res: list = os.listdir(Application.ABSOLUTE_BACKUP_DIR)
        except FileNotFoundError:
            return
        except Exception as e:
            logger.error(f'读取历史文件时发生错误,原因:"{e}"')
            return
        file_start: str = 'history_'
        file_end: str = '_config.yaml'

        now_timestamp = datetime.datetime.now().timestamp()  # 获取当前的时间戳
        if res:
            for i in res:  # 找出离当前时间最近的配置文件
                try:
                    if i.startswith(file_start) and i.endswith(file_end):
                        format_date_str = i.replace(file_start, '').replace(file_end, '').replace('_', ' ')
                        to_datetime_obj = datetime.datetime.strptime(format_date_str, '%Y-%m-%d %H-%M-%S')
                        timestamp = to_datetime_obj.timestamp()
                        self.history_timestamp[timestamp] = i
                except ValueError:
                    ...
                except Exception as e:
                    ...
            for i in self.history_timestamp.keys():
                self.difference_timestamp[now_timestamp - i] = i
            if self.history_timestamp:  # 如果有符合条件的历史配置文件
                self.last_record = self._find_history_config()

        else:
            return

    def config_guide(self):
        # input user to input necessary configurations
        # v1.1.0 更替api_id和api_hash位置,与telegram申请的api位置对应以免输错
        undefined = '无'

        def get_api_id(_last_record):
            while True:
                try:
                    api_id = console.input(
                        f'请输入「api_id」上一次的记录是:「{_last_record if _last_record else undefined}」:')
                    if api_id == '' and _last_record is not None:
                        api_id = _last_record
                    if Validator.is_valid_api_id(api_id):
                        self.config['api_id'] = api_id
                        console.print(f'已设置「api_id」为:「{api_id}」', style=self.color[0])
                        self.record_flag = True
                        break
                except KeyboardInterrupt:
                    self._keyboard_interrupt()

        def get_api_hash(_last_record, _valid_length):
            while True:
                try:
                    api_hash = console.input(
                        f'请输入「api_hash」上一次的记录是:「{_last_record if _last_record else undefined}」:')
                    if api_hash == '' and _last_record is not None:
                        api_hash = _last_record
                    if Validator.is_valid_api_hash(api_hash, _valid_length):
                        self.config['api_hash'] = api_hash
                        console.print(f'已设置「api_hash」为:「{api_hash}」', style=self.color[1])
                        self.record_flag = True
                        break
                    else:
                        logger.warning(f'意外的参数:"{api_hash}",不是一个「{_valid_length}位」的「值」!请重新输入!')
                except KeyboardInterrupt:
                    self._keyboard_interrupt()

        def get_links(_last_record, _valid_format):
            # 输入需要下载的媒体链接文件路径,确保文件存在
            links_file = None
            while True:
                try:
                    links_file = console.input(
                        f'请输入需要下载的媒体链接的「完整路径」。上一次的记录是:「{_last_record if _last_record else undefined}」格式 - 「{_valid_format}」:').strip()
                    if links_file == '' and _last_record is not None:
                        links_file = _last_record
                    if Validator.is_valid_links_file(links_file, _valid_format):
                        self.config['links'] = links_file
                        console.print(f'已设置「links_file」为:「{links_file}」', style=self.color[2])
                        self.record_flag = True
                        break
                    elif not os.path.normpath(links_file).endswith('.txt'):
                        logger.warning(f'意外的参数:"{links_file}",文件路径必须以「{_valid_format}」结尾,请重新输入!')
                    else:
                        logger.warning(
                            f'意外的参数:"{links_file}",文件路径必须以「{_valid_format}」结尾,并且「必须存在」,请重新输入!')
                except KeyboardInterrupt:
                    self._keyboard_interrupt()
                except Exception as e:
                    logger.error(f'意外的参数:"{links_file}",请重新输入!原因:"{e}"')

        def get_save_path(_last_record):
            # 输入媒体保存路径,确保是一个有效的目录路径
            while True:
                try:
                    save_path = console.input(
                        f'请输入媒体「保存路径」。上一次的记录是:「{_last_record if _last_record else undefined}」:').strip()
                    if save_path == '' and _last_record is not None:
                        save_path = _last_record
                    if Validator.is_valid_save_path(save_path):
                        self.config['save_path'] = save_path
                        console.print(f'已设置「save_path」为:「{save_path}」', style=self.color[3])
                        self.record_flag = True
                        break
                    elif os.path.isfile(save_path):
                        logger.warning(f'意外的参数:"{save_path}",指定的路径是一个文件并非目录,请重新输入!')
                    else:
                        logger.warning(f'意外的参数:"{save_path}",指定的路径无效或不是一个目录,请重新输入!')
                except KeyboardInterrupt:
                    self._keyboard_interrupt()

        def get_max_download_task(_last_record):
            # 输入最大下载任务数,确保是一个整数且不超过特定限制
            while True:
                try:
                    max_tasks = console.input(
                        f'请输入「最大下载任务数」。上一次的记录是:「{_last_record if _last_record else undefined}」,非会员不建议大于「5」,容易被限制为强制单任务下载{"(默认3)" if _last_record is None else ""}:').strip()
                    if max_tasks == '' and _last_record is not None:
                        max_tasks = _last_record
                    if max_tasks == '':
                        max_tasks = 3
                    if Validator.is_valid_max_download_task(max_tasks):
                        self.config['max_download_task'] = int(max_tasks)
                        console.print(f'已设置「max_download_task」为:「{max_tasks}」', style=self.color[4])
                        self.record_flag = True
                        break
                    else:
                        logger.warning(f'意外的参数:"{max_tasks}",任务数必须是「正整数」,请重新输入!')
                except KeyboardInterrupt:
                    self._keyboard_interrupt()
                except Exception as e:
                    logger.error(f'意外的错误,原因:"{e}"')

        def get_is_shutdown(_last_record, _valid_format):
            if _last_record:
                _last_record = 'y'
            elif _last_record is False:
                _last_record = 'n'
            else:
                _last_record = undefined
            while True:
                try:
                    question = console.input(
                        f'下载完成后是否「自动关机」。上一次的记录是:「{_last_record}」 - 「{_valid_format}」{"(默认n)" if _last_record == undefined else ""}:').strip()
                    if question == '' and _last_record != undefined:
                        if _last_record == 'y':
                            self.config['is_shutdown'] = True
                            console.print(f'已设置「is_shutdown」为:「{_last_record}」,下载完成后将自动关机!',
                                          style=self.color[5])
                            self.record_flag = True
                            break
                        elif _last_record == 'n':
                            self.config['is_shutdown'] = False
                            console.print(f'已设置「is_shutdown」为:「{_last_record}」', style=self.color[5])
                            self.record_flag = True
                            break
                    elif question == 'y':
                        self.config['is_shutdown'] = True
                        console.print(f'已设置「is_shutdown」为:「{question}」,下载完成后将自动关机!', style='Pink1')
                        self.record_flag = True
                        break
                    elif question == 'n' or question == '':
                        self.config['is_shutdown'] = False
                        console.print(f'已设置「is_shutdown」为:「n」', style=self.color[5])
                        self.record_flag = True
                        break
                    else:
                        logger.warning(f'意外的参数:"{question}",支持的参数 - 「{_valid_format}」')
                except KeyboardInterrupt:
                    self._keyboard_interrupt()
                except Exception as e:
                    logger.error(f'意外的错误,原因:"{e}"')
                    break

        if any([
            not self.config.get('api_id'),
            not self.config.get('api_hash'),
            not self.config.get('links'),
            not self.config.get('save_path'),
            not self.config.get('max_download_task'),
            not self.config.get('proxy'),
            not (self.config.get('proxy') or {}).get('enable_proxy', False),
            not (self.config.get('proxy') or {}).get('hostname', False),
            not (self.config.get('proxy') or {}).get('is_notice', False),
            not (self.config.get('proxy') or {}).get('username', False),
            not (self.config.get('proxy') or {}).get('password', False),
            not (self.config.get('proxy') or {}).get('scheme', False)
        ]):
            console.print('「注意」直接回车代表使用上次的记录。', style='red')
        if not self.config.get('api_id'):
            last_record = self.last_record.get('api_id')
            get_api_id(_last_record=last_record)
        if not self.config.get('api_hash'):
            valid_length: int = 32
            last_record = self.last_record.get('api_hash')
            get_api_hash(_last_record=last_record, _valid_length=valid_length)
        if not self.config.get('links'):
            valid_format: str = '.txt'
            last_record = self.last_record.get('links')
            get_links(_last_record=last_record, _valid_format=valid_format)
        if not self.config.get('save_path'):
            last_record = self.last_record.get('save_path')
            get_save_path(_last_record=last_record)
        if not self.config.get('max_download_task'):
            last_record = self.last_record.get('max_download_task') if self.last_record.get(
                'max_download_task') else None
            get_max_download_task(_last_record=last_record)
        # v1.1.6下载完成自动关机
        last_record = self.last_record.get('is_shutdown')
        valid_format = 'y|n'
        get_is_shutdown(_last_record=last_record, _valid_format=valid_format)

        proxy_config: dict = self.config.get('proxy', {})  # 读取proxy字段得到字典
        # v1.1.4 移除self._check_proxy_params(proxy_config)改用全字段检测  # 检查代理字典字段是否完整并自动补全保存
        enable_proxy = self.config.get('proxy') or {}.get('enable_proxy', False)
        proxy_record = self.last_record.get('proxy') if self.last_record.get('proxy') else {}

        def get_proxy_info(_scheme, _hostname, _port):
            if _scheme is None:
                _scheme = proxy_record.get('scheme', '未知')
            if _hostname is None:
                _hostname = proxy_record.get('hostname', '未知')
            if _port is None:
                _port = proxy_record.get('port', '未知')
            return _scheme, _hostname, _port

        if proxy_config.get('is_notice') is True or proxy_config.get('is_notice') is None:  # 如果打开了通知或第一次配置
            ep_last_record = proxy_record.get('enable_proxy', False)
            in_last_record = proxy_record.get('is_notice', False)
            if ep_last_record:
                ep_notice = 'y' if ep_last_record else 'n'
            else:
                ep_notice = undefined
            if in_last_record:
                in_notice = 'y' if in_last_record else 'n'
            else:
                in_notice = undefined
            valid_format = 'y|n'

            try:
                while True:
                    enable_proxy = console.input(
                        f'是否需要使用「代理」。上一次的记录是:「{ep_notice}」 - 「{valid_format}」{"(默认n)" if ep_notice == undefined else ""}:').lower()  # 询问是否开启代理
                    if enable_proxy == '' and ep_last_record is not None:
                        if ep_last_record is True:
                            enable_proxy = 'y'
                        elif ep_last_record is False:
                            enable_proxy = 'n'
                    elif enable_proxy == '':
                        enable_proxy = 'n'
                    if Validator.is_valid_enable_proxy(enable_proxy):
                        if enable_proxy == 'y':
                            proxy_config['enable_proxy'] = True
                        elif enable_proxy == 'n':
                            proxy_config['enable_proxy'] = False
                        console.print(f'已设置「enable_proxy」为:「{enable_proxy}」', style=self.color[6])
                        self.record_flag = True
                        break
                    else:
                        logger.error(f'意外的参数:"{enable_proxy}",请输入有效参数! - 「{valid_format}」!')
                while True:
                    # 是否记住选项
                    is_notice = console.input(
                        f'下次是否「不再询问使用代理」。上一次的记录是:「{in_notice}」 - 「{valid_format}」{("(默认n)" if in_notice == undefined else "")}:').lower()
                    if is_notice == '' and in_last_record is not None:
                        if in_last_record is True:
                            is_notice = 'y'
                        elif in_last_record is False:
                            is_notice = 'n'
                    elif is_notice == '':
                        is_notice = 'n'
                    if Validator.is_valid_is_notice(is_notice):
                        if is_notice == 'y':
                            proxy_config['is_notice'] = False
                            console.print('下次将不再询问是否使用代理!', style='green')
                        elif is_notice == 'n':
                            proxy_config['is_notice'] = True
                        console.print(f'已设置「is_notice」为:「{is_notice}」', style=self.color[7])
                        self.record_flag = True
                        break
                    else:
                        logger.error(f'意外的参数:"{is_notice}",请输入有效参数! - 「{valid_format}」!')

            except KeyboardInterrupt:
                self._keyboard_interrupt()

        if enable_proxy == 'y' or enable_proxy is True:
            scheme = None
            hostname = None
            port = None
            if self._is_proxy_input(proxy_config):
                valid_port = '0~65535'
                # 输入代理类型
                if not proxy_config['scheme']:
                    valid_format: list = ['http', 'socks4', 'socks5']
                    last_record = proxy_record.get('scheme')
                    while True:
                        try:
                            scheme = console.input(
                                f'请输入「代理类型」。上一次的记录是:「{last_record if last_record else undefined}」 - 「{"|".join(valid_format)}」:').strip().lower()
                            if scheme == '' and last_record is not None:
                                scheme = last_record
                            if Validator.is_valid_scheme(scheme, valid_format):
                                proxy_config['scheme'] = scheme
                                self.record_flag = True
                                console.print(f'已设置「scheme」为:「{scheme}」', style=self.color[9])
                                break
                            else:
                                logger.warning(
                                    f'意外的参数:"{scheme}",请输入有效的代理类型! - 「{"|".join(valid_format)}」!')
                        except KeyboardInterrupt:
                            self._keyboard_interrupt()
                if not proxy_config.get('hostname'):
                    valid_format: str = 'x.x.x.x'
                    last_record = self.last_record.get('proxy', {}).get('hostname')
                    while True:
                        scheme, _, __ = get_proxy_info(scheme, None, None)
                        # 输入代理IP地址
                        try:
                            hostname = console.input(
                                f'请输入代理类型为:"{scheme}"的「ip地址」。上一次的记录是:「{last_record if last_record else undefined}」 - 「{valid_format}」:').strip()
                            if hostname == '' and last_record is not None:
                                hostname = last_record
                            if Validator.is_valid_hostname(hostname):
                                proxy_config['hostname'] = hostname
                                self.record_flag = True
                                console.print(f'已设置「hostname」为:「{hostname}」', style=self.color[10])
                                break
                        except ValueError:
                            logger.warning(f'"{hostname}"不是一个「ip地址」,请输入有效的ipv4地址! - 「{valid_format}」!')
                        except KeyboardInterrupt:
                            self._keyboard_interrupt()
                if not proxy_config.get('port'):
                    last_record = self.last_record.get('proxy', {}).get('port')
                    # 输入代理端口
                    while True:
                        try:  # hostname，scheme可能出现None
                            scheme, hostname, __ = get_proxy_info(scheme, hostname, None)
                            port = console.input(
                                f'请输入ip地址为:"{hostname}",代理类型为:"{scheme}"的「代理端口」。上一次的记录是:「{last_record if last_record else undefined}」 - 「{valid_port}」:').strip()
                            if port == '' and last_record is not None:
                                port = last_record
                            if Validator.is_valid_port(port):
                                proxy_config['port'] = int(port)
                                self.record_flag = True
                                console.print(f'已设置「port」为:「{port}」', style=self.color[11])
                                break
                            else:
                                logger.warning(f'意外的参数:"{port}",端口号必须在「{valid_port}」之间!')
                        except ValueError:
                            logger.warning(f'意外的参数:"{port}",请输入一个有效的整数! - 「{valid_port}」')
                        except KeyboardInterrupt:
                            self._keyboard_interrupt()
                        except Exception as e:
                            logger.error(f'意外的错误,原因:"{e}"')
                if not all([proxy_config.get('username'), proxy_config.get('password')]):
                    # 是否需要认证
                    while True:
                        try:
                            is_proxy = console.input(f'代理是否需要「认证」? - 「y|n」(默认n):').strip().lower()
                            if is_proxy == 'y':
                                try:
                                    proxy_config['username'] = console.input('请输入「用户名」:').strip()
                                    self.record_flag = True
                                    proxy_config['password'] = console.input('请输入「密码」:').strip()
                                    self.record_flag = True
                                    console.print(f'已设置为:「代理需要认证」', style=self.color[12])
                                except KeyboardInterrupt:
                                    self._keyboard_interrupt()
                                finally:
                                    break
                            elif is_proxy == 'n' or is_proxy == '':
                                proxy_config['username'] = None
                                proxy_config['password'] = None
                                console.print(f'已设置为:「代理不需要认证」', style=self.color[12])
                                break
                        except KeyboardInterrupt:
                            self._keyboard_interrupt()
        self.save_config()
        return


class PanelTable:
    def __init__(self, title: str, header: tuple, data: list, styles: dict = None):
        self.table = Table(title=title, highlight=True)
        from rich.table import Style
        self.table.title_style = Style(color='white', bold=True)
        # 添加列
        for i, col in enumerate(header):
            style = styles.get(col, {}) if styles else {}
            self.table.add_column(col, **style)

        # 添加数据行
        for row in data:
            self.table.add_row(*map(str, row))  # 确保数据项是字符串类型，防止类型错误

    def print_meta(self):
        console.print(self.table, justify='center')


class MetaData:
    @staticmethod
    def pay():
        if check_run_env():  # 是终端才打印,生产环境会报错
            console.print(qrterm.draw('wxp://f2f0g8lKGhzEsr0rwtKWTTB2gQzs9Xg9g31aBvlpbILowMTa5SAMMEwn0JH1VEf2TGbS'),
                          justify='center')
            console.print(
                GradientColor.gen_gradient_text(text='欢迎微信扫码支持作者!',
                                                gradient_color=GradientColor.yellow_to_green),
                justify='center')

    @staticmethod
    def print_meta():
        console.print(GradientColor.gen_gradient_text(
            text=ArtFont.author_art_3,
            gradient_color=GradientColor.generate_gradient(
                start_color='#fa709a',
                end_color='#fee140',
                steps=10)),
            style='blink',
            highlight=False)
        console.print(f'[bold]{SOFTWARE_FULL_NAME} v{__version__}[/bold],\n[i]{__copyright__}[/i]'
                      )
        console.print(f'Licensed under the terms of the {__license__}', end='\n')
        console.print(GradientColor.gen_gradient_text('\t软件免费使用!并且在GitHub开源,如果你付费那就是被骗了。',
                                                      gradient_color=GradientColor.blue_to_purple))


def print_helper():
    config_helper = r'''
# 配置文件说明
```yaml
# 下载完成直接打开软件即可,软件会一步一步引导你输入的!这里只是介绍每个参数的含义
# 填入第一步教你申请的api_hash和api_id
# 如果是按照软件的提示填,不需要加引号,如果是手动打开config.yaml修改配置,请仔细阅读下面内容
# 手动填写注意区分冒号类型,例如 - 是:不是：
# 手动填写的时候还请注意参数冒号不加空格会报错 后面有一个空格,例如 - api_hash: xxx而不是api_hash:xxx
api_hash: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx #api_hash没有引号
api_id: 'xxxxxxxx' #注意配置文件中只有api_id有引号！！！
links: D:\path\where\your\link\txt\save\content.txt # 链接地址写法如下:
# 新建txt文本,一个链接为一行,将路径填入即可请不要加引号,在软件运行前就准备好
# D:\path\where\your\link\txt\save\content.txt 请注意一个链接一行
# 列表写法已在v1.1.0版本中弃用,目前只有上述唯一写法！！！
# 不要存在中文或特殊字符
max_download_task: 3 # 最大的同时下载任务数 注意:如果你不是Telegram会员,那么最大同时下载数只有1
proxy: # 代理部分,如不使用请全部填null注意冒号后面有空格,否则不生效导致报错!
  enable_proxy: true # 是否开启代理 true为开启 false为关闭
  hostname: 127.0.0.1 # 代理的ip地址
  is_notice: false # 是否开启代理提示, true为每次打开询问你是否开启代理, false则为关闭
  scheme: socks5 # 代理的类型,支持http,socks4,socks5
  port: 10808 # 代理ip的端口
  username: null # 代理的账号,有就填,没有请都填null!
  password: null # 代理的密码,有就填,没有请都填null!
save_path: F:\path\the\media\where\you\save # 下载的媒体保存的地址,没有引号,不要存在中文或特殊字符
# 再次提醒,由于nuitka打包的性质决定,中文路径无法被打包好的二进制文件识别,故在配置文件时无论是链接路径还是媒体保存路径都请使用英文命名。
is_shutdown: true # 是否下载完成后自动关机 true为下载完成后自动关机 false为下载完成后不关机
```
'''
    markdown = Markdown(config_helper)
    console.print(markdown)

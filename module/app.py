# coding=UTF-8
# Author:Gentlesprite
# Software:PyCharm
# Time:2024/7/25 12:32
# File:app.py
import os
import sys
import time
import qrcode
import platform
import mimetypes
import datetime
import subprocess
import pyrogram

from typing import Dict
from functools import wraps
from pyrogram.errors import FloodWait
from rich.markdown import Markdown
from rich.table import Table, Style
from rich.progress import Progress, TextColumn, BarColumn, TimeRemainingColumn, TransferSpeedColumn

from module import yaml
from module import CustomDumper
from module import readme
from module import console, log
from module import SOFTWARE_FULL_NAME, __version__, __copyright__, __license__

from module.process_path import split_path, validate_title, truncate_filename, move_to_save_path, \
    gen_backup_config, get_extension, safe_delete
from module.enum_define import GradientColor, ArtFont, DownloadType, DownloadStatus, Validator, QrcodeRender
from module.enum_define import failure_download, keyword_size, keyword_link_status, keyword_file, keyword_type, \
    keyword_error_size, keyword_actual_size


class TelegramRestrictedMediaDownloaderClient(pyrogram.Client):

    async def authorize(self) -> pyrogram.types.User:
        if self.bot_token:
            return await self.sign_in_bot(self.bot_token)
        console.print(
            f'Pyrogram is free software and comes with ABSOLUTELY NO WARRANTY. Licensed\n'
            f'under the terms of the {pyrogram.__license__}.')
        console.print(
            f'欢迎使用[#b4009e]{SOFTWARE_FULL_NAME}[/#b4009e](版本 {__version__})'
            f'基于Pyrogram(版本 {pyrogram.__version__})。')
        while True:
            try:
                if not self.phone_number:
                    while True:
                        value = console.input('请输入「电话号码」或「bot token」([#6a2c70]电话号码[/#6a2c70]需以[#b83b5e]「+地区」'
                                              '[/#b83b5e]开头!如:[#f08a5d]+86[/#f08a5d][#f9ed69]15000000000[/#f9ed69]):').strip()
                        if not value:
                            continue

                        confirm = console.input(
                            f'所输入的「{value}」是否[green]正确[/green]? - 「y|n」(默认y): ').strip().lower()

                        if confirm == 'y' or confirm == '':
                            break
                        else:
                            log.warning(f'意外的参数:"{confirm}",支持的参数 - 「y|n」(默认y)')
                    if ':' in value:
                        self.bot_token = value
                        return await self.sign_in_bot(value)
                    else:
                        self.phone_number = value

                sent_code = await self.send_code(self.phone_number)
            except pyrogram.errors.BadRequest as e:
                console.print(e.MESSAGE)
                self.phone_number = None
                self.bot_token = None
            else:
                break

        sent_code_descriptions = {
            pyrogram.enums.SentCodeType.APP: 'Telegram app',
            pyrogram.enums.SentCodeType.SMS: 'SMS',
            pyrogram.enums.SentCodeType.CALL: 'phone call',
            pyrogram.enums.SentCodeType.FLASH_CALL: 'phone flash call',
            pyrogram.enums.SentCodeType.FRAGMENT_SMS: 'Fragment SMS',
            pyrogram.enums.SentCodeType.EMAIL_CODE: 'email code'
        }

        console.print(
            f'[#f08a5d]「验证码」[/#f08a5d]已通过[#f9ed69]「{sent_code_descriptions[sent_code.type]}」[/#f9ed69]发送。')

        while True:
            if not self.phone_code:
                self.phone_code = console.input('请输入收到的[#f08a5d]「验证码」[/#f08a5d]:').strip()

            try:
                signed_in = await self.sign_in(self.phone_number, sent_code.phone_code_hash, self.phone_code)
            except pyrogram.errors.BadRequest as e:
                console.print(e.MESSAGE)
                self.phone_code = None
            except pyrogram.errors.SessionPasswordNeeded as _:
                console.print(
                    '当前登录账号设置了[#f08a5d]「两步验证」[/#f08a5d],需要提供两步验证的[#f9ed69]「密码」[/#f9ed69]。')

                while True:
                    console.print('密码提示:{}'.format(await self.get_password_hint()))

                    if not self.password:
                        self.password = console.input(
                            '输入[#f08a5d]「两步验证」[/#f08a5d]的[#f9ed69]「密码」[/#f9ed69](为空代表忘记密码):',
                            password=self.hide_password).strip()

                    try:
                        if not self.password:
                            confirm = console.input(
                                '确认[#f08a5d]「恢复密码」[/#f08a5d]? - 「y|n」(默认y):').strip().lower()

                            if confirm == 'y' or confirm == '':
                                email_pattern = await self.send_recovery_code()
                                console.print(
                                    f'[#f08a5d]「恢复代码」[/#f08a5d]已发送到邮箱[#f9ed69]「{email_pattern}」[/#f9ed69]。')

                                while True:
                                    recovery_code = console.input('请输入[#f08a5d]「恢复代码」[/#f08a5d]:').strip()

                                    try:
                                        return await self.recover_password(recovery_code)
                                    except pyrogram.errors.BadRequest as e:
                                        console.print(e.MESSAGE)
                                    except Exception as _:
                                        console.print_exception()
                                        raise
                            else:
                                self.password = None
                        else:
                            return await self.check_password(self.password)
                    except pyrogram.errors.BadRequest as e:
                        console.print(e.MESSAGE)
                        self.password = None
            else:
                break

        if isinstance(signed_in, pyrogram.types.User):
            return signed_in

        while True:
            first_name = console.input('输入[#f08a5d]「名字」[/#f08a5d]:').strip()
            last_name = console.input('输入[#f9ed69]「姓氏」[/#f9ed69](为空代表跳过): ').strip()

            try:
                signed_up = await self.sign_up(
                    self.phone_number,
                    sent_code.phone_code_hash,
                    first_name,
                    last_name
                )
            except pyrogram.errors.BadRequest as e:
                console.print(e.MESSAGE)
            else:
                break

        if isinstance(signed_in, pyrogram.types.TermsOfService):
            console.print('\n' + signed_in.text + '\n')
            await self.accept_terms_of_service(signed_in.id)

        return signed_up


class Application:
    # 将 None 的表示注册到 Dumper 中。

    DIR_NAME: str = os.path.dirname(os.path.abspath(sys.argv[0]))  # 获取软件工作绝对目录。
    CONFIG_NAME: str = 'config.yaml'  # 配置文件名。
    CONFIG_PATH: str = os.path.join(DIR_NAME, CONFIG_NAME)
    CONFIG_TEMPLATE: dict = {
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
        'is_shutdown': None,
        'download_type': None
    }
    TEMP_FOLDER: str = os.path.join(os.getcwd(), 'temp')
    BACKUP_DIR: str = 'ConfigBackup'
    ABSOLUTE_BACKUP_DIR: str = os.path.join(DIR_NAME, BACKUP_DIR)
    WORK_DIR: str = os.path.join(os.getcwd(), 'sessions')

    def __init__(self,
                 client_obj: callable = TelegramRestrictedMediaDownloaderClient,
                 guide: bool = True):
        self.client_obj: callable = client_obj
        self.platform: str = MetaData.get_platform().get('system')
        self.color: list = GradientColor.blue_to_purple
        self.history_timestamp: dict = {}
        self.input_link: list = []
        self.last_record: dict = {}
        self.difference_timestamp: dict = {}
        self.download_type: list = []
        self.record_dtype: set = set()
        self.config_path: str = Application.CONFIG_PATH
        self.work_dir: str = Application.WORK_DIR
        self.temp_folder: str = Application.TEMP_FOLDER
        self.record_flag: bool = False
        self.modified: bool = False
        self.get_last_history_record()
        self._config = self.load_config()  # v1.2.9 重新调整配置文件加载逻辑。
        self.config_guide() if guide else 0
        self.config = self.load_config()
        self.api_hash = self.config.get('api_hash')
        self.api_id = self.config.get('api_id')
        self.download_type: list = self.config.get('download_type')
        self.is_shutdown: bool = self.config.get('is_shutdown')
        self.links: str = self.config.get('links')
        self.max_download_task: int = self.config.get('max_download_task')
        self.proxy: dict = self.config.get('proxy', {})
        self.enable_proxy = self.proxy if self.proxy.get('enable_proxy') else None
        self.save_path: str = self.config.get('save_path')
        self._get_download_type()
        self.current_task_num: int = 0
        self.max_retry_count: int = 3
        self.skip_video, self.skip_photo = set(), set()
        self.success_video, self.success_photo = set(), set()
        self.failure_video, self.failure_photo = set(), set()
        self.failure_link: dict = {}  # v1.1.2
        self.progress = Progress(TextColumn('[bold blue]{task.fields[filename]}', justify='right'),
                                 BarColumn(bar_width=40),
                                 '[progress.percentage]{task.percentage:>3.1f}%',
                                 '•',
                                 '[bold green]{task.fields[info]}',
                                 '•',
                                 TransferSpeedColumn(),
                                 '•',
                                 TimeRemainingColumn(),
                                 console=console
                                 )

    @staticmethod
    def download_bar(current, total, progress, task_id):
        progress.update(task_id,
                        completed=current,
                        info=f'{MetaData.suitable_units_display(current)}/{MetaData.suitable_units_display(total)}',
                        total=total)

    def build_client(self) -> pyrogram.Client:
        """用填写的配置文件,构造pyrogram客户端。"""
        os.makedirs(self.work_dir, exist_ok=True)
        return self.client_obj(name=SOFTWARE_FULL_NAME.replace(' ', ''),
                               api_id=self.api_id,
                               api_hash=self.api_hash,
                               proxy=self.enable_proxy,
                               workdir=self.work_dir)

    def print_media_table(self):
        """打印统计的下载信息的表格。"""
        header: tuple = ('种类&状态', '成功下载', '失败下载', '跳过下载', '合计')
        self.download_type.remove(DownloadType.document.text) if DownloadType.document.text in self.download_type else 0
        success_video: int = len(self.success_video)
        failure_video: int = len(self.failure_video)
        skip_video: int = len(self.skip_video)
        success_photo: int = len(self.success_photo)
        failure_photo: int = len(self.failure_photo)
        skip_photo: int = len(self.skip_photo)
        total_video: int = sum([success_video, failure_video, skip_video])
        total_photo: int = sum([success_photo, failure_photo, skip_photo])
        rdt_length: int = len(self.record_dtype)
        if rdt_length == 1:
            _compare_dtype: list = list(self.record_dtype)[0]
            if _compare_dtype == DownloadType.video.text:  # 只有视频的情况。
                video_table = PanelTable(title='视频下载统计',
                                         header=header,
                                         data=[
                                             [DownloadType.translate(DownloadType.video.text),
                                              success_video,
                                              failure_video,
                                              skip_video,
                                              total_video],
                                             ['合计', success_video,
                                              failure_video,
                                              skip_video,
                                              total_video]
                                         ]
                                         )
                video_table.print_meta()
            if _compare_dtype == DownloadType.photo.text:  # 只有图片的情况。
                photo_table = PanelTable(title='图片下载统计',
                                         header=header,
                                         data=[
                                             [DownloadType.translate(DownloadType.photo.text),
                                              success_photo,
                                              failure_photo,
                                              skip_photo,
                                              total_photo],
                                             ['合计', success_photo,
                                              failure_photo,
                                              skip_photo,
                                              total_photo]
                                         ]
                                         )
                photo_table.print_meta()
        elif rdt_length == 2:
            media_table = PanelTable(title='媒体下载统计',
                                     header=header,
                                     data=[
                                         [DownloadType.translate(DownloadType.video.text),
                                          success_video,
                                          failure_video,
                                          skip_video,
                                          total_video],
                                         [DownloadType.translate(DownloadType.photo.text),
                                          success_photo,
                                          failure_photo,
                                          skip_photo,
                                          total_photo],
                                         ['合计', sum([success_video, success_photo]),
                                          sum([failure_video, failure_photo]),
                                          sum([skip_video, skip_photo]),
                                          sum([total_video, total_photo])]
                                     ])
            media_table.print_meta()

    def print_failure_table(self):
        """打印统计的下载过程中失败信息的表格。"""
        format_failure_info: list = []
        for index, (key, value) in enumerate(self.failure_link.items(), start=1):
            format_failure_info.append([index, key, value])
        failure_link_table = PanelTable(title='失败链接统计',
                                        header=('编号', '链接', '原因'),
                                        data=format_failure_info)
        failure_link_table.print_meta()

    def process_shutdown(self, second: int):
        """处理关机逻辑。"""
        self.shutdown_task(second=second) if self.is_shutdown else 0

    def check_download_finish(self, sever_size: int, download_path: str, save_directory: str) -> bool:
        """检测文件是否下完。"""
        temp_ext: str = '.temp'
        if os.path.exists(download_path) or os.path.exists(download_path + temp_ext):
            try:
                local_size: int = os.path.getsize(download_path)
            except FileNotFoundError:
                local_size: int = os.path.getsize(download_path + temp_ext)  # v1.2.9 修复临时文件大小获取失败的问题。
        else:
            local_size: int = 0  # 仍然找不到则直接为0
        format_local_size: str = MetaData.suitable_units_display(local_size)
        format_sever_size: str = MetaData.suitable_units_display(sever_size)
        _save_path: str = os.path.join(save_directory, split_path(download_path).get('file_name'))
        save_path: str = _save_path[:-len(temp_ext)] if _save_path.endswith(temp_ext) else _save_path
        if sever_size == local_size:
            result: str = move_to_save_path(temp_save_path=download_path, save_path=save_directory).get('e_code')
            console.warning(result) if result is not None else 0
            console.log(
                f'{keyword_file}:"{save_path}",'
                f'{keyword_size}:{format_local_size},'
                f'{keyword_type}:{DownloadType.translate(self.guess_file_type(file_name=download_path, status=DownloadStatus.success)[0].text)},'
                f'{keyword_link_status}:{DownloadStatus.translate(DownloadStatus.success.text)}。',
            )
            return True
        else:
            console.log(
                f'{keyword_file}:"{save_path}",'
                f'{keyword_error_size}:{format_local_size},'
                f'{keyword_actual_size}:{format_sever_size},'
                f'{keyword_type}:{DownloadType.translate(self.guess_file_type(file_name=download_path, status=DownloadStatus.failure)[0].text)},'
                f'{keyword_link_status}:{failure_download}。')
            safe_delete(file_path=download_path)  # v1.2.9 修复临时文件删除失败的问题。
            return False

    def get_media_meta(self, message, dtype) -> dict:
        """获取媒体元数据。"""
        temp_save_path: str = self._get_temp_path(message, dtype)
        _sever_meta = getattr(message, dtype)
        sever_size: int = getattr(_sever_meta, 'file_size')
        file_name: str = split_path(temp_save_path).get('file_name')
        local_file_path: str = os.path.join(self.save_path, file_name)
        format_file_size: str = MetaData.suitable_units_display(sever_size)
        return {'temp_save_path': temp_save_path,
                'sever_size': sever_size,
                'file_name': file_name,
                'local_file_path': local_file_path,
                'format_file_size': format_file_size}

    def get_valid_dtype(self, message) -> Dict[str, bool]:
        """获取媒体类型是否与所需下载的类型相匹配。"""
        valid_dtype = next((i for i in DownloadType.support_type() if getattr(message, i, None)),
                           None)  # 判断该链接是否为视频或图片,文档。
        is_document_type_valid = None
        # 当媒体文件是文档形式的,需要根据配置需求将视频和图片过滤出来。
        if getattr(message, 'document'):
            mime_type = message.document.mime_type  # 获取 document 的 mime_type 。
            # 只下载视频的情况。
            if DownloadType.video.text in self.download_type and DownloadType.photo.text not in self.download_type:
                if 'video' in mime_type:
                    is_document_type_valid = True  # 允许下载视频。
                elif 'image' in mime_type:
                    is_document_type_valid = False  # 跳过下载图片。
            # 只下载图片的情况。
            elif DownloadType.photo.text in self.download_type and DownloadType.video.text not in self.download_type:
                if 'video' in mime_type:
                    is_document_type_valid = False  # 跳过下载视频。
                elif 'image' in mime_type:
                    is_document_type_valid = True  # 允许下载图片。
            else:
                is_document_type_valid = True
        else:
            is_document_type_valid = True
        return {'valid_dtype': valid_dtype,
                'is_document_type_valid': is_document_type_valid}

    def _get_temp_path(self, message: pyrogram.types.Message,
                       dtype: DownloadType.text) -> str:
        """获取下载文件时的临时保存路径。"""
        file_name = None
        os.makedirs(self.temp_folder, exist_ok=True)

        def _process_video(msg_obj: pyrogram.types, _dtype: DownloadType.text):
            """处理视频文件的逻辑。"""
            _default_mtype: str = 'video/mp4'  # v1.2.8 健全获取文件名逻辑。
            _meta_obj = getattr(msg_obj, _dtype)
            _title = getattr(_meta_obj, 'file_name', None)  # v1.2.8 修复当文件名不存在时,下载报错问题。
            try:
                if _title is None:
                    _title = 'None'
                else:
                    _title = os.path.splitext(_title)[0]
            except Exception as e:
                _title = 'None'
                log.warning(f'获取文件名时出错,已重命名为:"{_title}",原因:"{e}"')
            _file_name = '{} - {}.{}'.format(
                getattr(msg_obj, 'id', 'None'),
                _title,
                get_extension(file_id=_meta_obj.file_id, mime_type=getattr(_meta_obj, 'mime_type', _default_mtype),
                              dot=False)
            )
            _file_name = os.path.join(self.temp_folder, validate_title(_file_name))
            return _file_name

        def _process_photo(msg_obj: pyrogram.types, _dtype: DownloadType.text):
            """处理视频图片的逻辑。"""
            _default_mtype: str = 'image/jpg'  # v1.2.8 健全获取文件名逻辑。
            _meta_obj = getattr(msg_obj, _dtype)
            _extension: str = 'unknown'
            if _dtype == DownloadType.photo.text:
                _extension = get_extension(file_id=_meta_obj.file_id, mime_type=_default_mtype,
                                           dot=False)
            elif _dtype == DownloadType.document.text:
                _extension = get_extension(file_id=_meta_obj.file_id,
                                           mime_type=getattr(_meta_obj, 'mime_type', _default_mtype),
                                           dot=False)
            _file_name = '{} - {}.{}'.format(
                getattr(msg_obj, 'id'),
                getattr(_meta_obj, 'file_unique_id', 'None'),
                _extension
            )
            _file_name = os.path.join(self.temp_folder, validate_title(_file_name))
            return _file_name

        if dtype == DownloadType.video.text:
            file_name = _process_video(msg_obj=message, _dtype=dtype)
        elif dtype == DownloadType.photo.text:
            file_name = _process_photo(msg_obj=message, _dtype=dtype)
        elif dtype == DownloadType.document.text:
            _mime_type = getattr(getattr(message, dtype), 'mime_type')
            if 'video' in _mime_type:
                file_name = _process_video(msg_obj=message, _dtype=dtype)
            elif 'image' in _mime_type:
                file_name = _process_photo(msg_obj=message, _dtype=dtype)
        return truncate_filename(file_name)

    def _media_counter(func):
        """统计媒体下载情况(数量)的装饰器。"""

        @wraps(func)
        def wrapper(self, file_name, status):
            res = func(self, file_name, status)
            file_type, status = res
            if file_type == DownloadType.photo:
                if status == DownloadStatus.success:
                    self.success_photo.add(file_name)
                elif status == DownloadStatus.failure:
                    self.failure_photo.add(file_name)
                elif status == DownloadStatus.skip:
                    self.skip_photo.add(file_name)
                elif status == DownloadStatus.downloading:
                    self.current_task_num += 1
            elif file_type == DownloadType.video:
                if status == DownloadStatus.success:
                    self.success_video.add(file_name)
                elif status == DownloadStatus.failure:
                    self.failure_video.add(file_name)
                elif status == DownloadStatus.skip:
                    self.skip_video.add(file_name)
                elif status == DownloadStatus.downloading:
                    self.current_task_num += 1
            # v1.2.9 修复失败时重新下载时会抛出RuntimeError的问题。
            if self.failure_video and self.success_video:
                self.failure_video -= self.success_video  # 直接使用集合的差集操作。
            if self.failure_photo and self.success_photo:
                self.failure_photo -= self.success_photo
            return res

        return wrapper

    @_media_counter
    def guess_file_type(self, file_name, status):
        """预测文件类型。"""
        result = ''
        file_type, _ = mimetypes.guess_type(file_name)
        if file_type is not None:
            file_main_type: str = file_type.split('/')[0]
            if file_main_type == 'image':
                result = DownloadType.photo
            elif file_main_type == 'video':
                result = DownloadType.video
        return result, status

    def _get_download_type(self):
        """获取需要下载的文件类型。"""
        if self.download_type is not None and (
                DownloadType.video.text in self.download_type or DownloadType.photo.text in self.download_type):
            self.record_dtype.update(self.download_type)  # v1.2.4 修复特定情况结束后不显示表格问题。
            self.download_type.append(DownloadType.document.text)
        else:
            self.download_type: list = DownloadType.support_type()
            self.record_dtype: set = {DownloadType.video.text,
                                      DownloadType.photo.text}  # v1.2.4 修复此处报错问题v1.2.3此处有致命错误。
            console.log(f'已使用默认下载类型:3.视频和图片。')

    def print_config_table(self):
        """打印用户所填写配置文件的表格。"""
        try:
            if self.enable_proxy:
                console.log(GradientColor.gen_gradient_text(
                    text='当前正在使用代理!',
                    gradient_color=GradientColor.green_to_blue))
                proxy_key: list = []
                proxy_value: list = []
                for i in self.proxy.items():
                    if i[0] not in ['username', 'password']:
                        key, value = i
                        proxy_key.append(key)
                        proxy_value.append(value)
                proxy_table = PanelTable(title='代理配置', header=tuple(proxy_key), data=[proxy_value])
                proxy_table.print_meta()
            else:
                console.log(GradientColor.gen_gradient_text(text='当前没有使用代理!',
                                                            gradient_color=GradientColor.new_life))
        except Exception as e:
            try:
                console.print(self.config)
            except Exception as _:
                log.exception(_, exc_info=False)
            log.exception(e, exc_info=False)
        try:
            # 展示链接内容表格。
            with open(file=self.links, mode='r', encoding='UTF-8') as _:
                res = [content.strip() for content in _.readlines()]
            format_res: list = []
            for i in enumerate(res, start=1):
                format_res.append(list(i))
            link_table = PanelTable(title='链接内容', header=('编号', '链接'),
                                    data=format_res)
            link_table.print_meta()
        except FileNotFoundError:  # v1.1.3 用户错误填写路径提示。
            log.error(f'读取"{self.links}"时出错。')
        except Exception as e:
            log.error(f'读取"{self.links}"时出错,原因:"{e}"')
        try:
            _dtype = self.download_type.copy()  # 浅拷贝赋值给_dtype,避免传入函数后改变原数据。
            data = [[DownloadType.translate(DownloadType.video.text),
                     self._get_dtype(_dtype).get('video')],
                    [DownloadType.translate(DownloadType.photo.text),
                     self._get_dtype(_dtype).get('photo')]]
            download_type_table = PanelTable(title='下载类型', header=('类型', '是否下载'), data=data)
            download_type_table.print_meta()

        except Exception as e:
            log.error(f'读取"{self.links}"时出错,原因:"{e}"')

    @staticmethod
    def ctrl_c():
        """处理Windows用户的按键中断。"""
        try:
            os.system('pause')
        except KeyboardInterrupt:
            pass

    @staticmethod
    def _get_dtype(download_dtype: list) -> dict:
        """获取所需下载文件的类型。"""
        if DownloadType.document.text in download_dtype:
            download_dtype.remove(DownloadType.document.text)
        if len(download_dtype) == 1:
            dtype = download_dtype[0]
            if dtype == DownloadType.video.text:
                return {'video': True, 'photo': False}
            elif dtype == DownloadType.photo.text:
                return {'video': False, 'photo': True}
        elif len(download_dtype) == 2:
            return {'video': True, 'photo': True}
        else:
            return {'error': True}

    def _stdio_style(self, key: str) -> str:
        """控制用户交互时打印出不同的颜色(渐变)。"""
        _stdio_queue = {'api_id': 0,
                        'api_hash': 1,
                        'links': 2,
                        'save_path': 3,
                        'max_download_task': 4,
                        'download_type': 5,
                        'is_shutdown': 6,
                        'enable_proxy': 7,
                        'is_notice': 8,
                        'config_proxy': 9,
                        'scheme': 10,
                        'hostname': 11,
                        'port': 12,
                        'proxy_authentication': 13
                        }
        return self.color[_stdio_queue.get(key)]

    def shutdown_task(self, second: int):
        """下载完成后自动关机的功能。"""
        try:
            if self.platform == 'Windows':
                # 启动关机命令 目前只支持对 Windows 系统的关机。
                shutdown_command = f'shutdown -s -t {second}'
                subprocess.Popen(shutdown_command, shell=True)  # 异步执行关机。
            elif self.platform == 'Linux' or self.platform == 'Darwin':
                # Linux 或 macOS 使用 shutdown 命令。
                shutdown_command = f'shutdown -h +{second // 60}'
                subprocess.Popen(shutdown_command, shell=True)  # 异步执行关机。
            # 实时显示倒计时。
            for remaining in range(second, 0, -1):
                console.print(f'即将在{remaining}秒后关机, 按「CTRL+C」可取消。', end='\r', style='#ff4805')
                time.sleep(1)
            console.print('\n关机即将执行!', style='#f6ad00')
        except KeyboardInterrupt:
            cancel_flag: bool = False
            # 如果用户按下 CTRL+C，取消关机。
            if self.platform == 'Windows':
                subprocess.Popen('shutdown -a', shell=True)  # 取消关机。
                cancel_flag = True
            else:
                try:
                    # Linux/macOS 取消关机命令。
                    subprocess.Popen('shutdown -c', shell=True)
                    cancel_flag = True
                except Exception as e:
                    log.warning(f'取消关机任务失败,可能是当前系统不支持,原因:"{e}"')
            console.print('\n关机已被用户取消!', style='#4bd898') if cancel_flag else 0
        except Exception as e:
            log.error(f'执行关机任务失败,可能是当前系统不支持自动关机,原因:"{e}"')

    def backup_config(self, backup_config: dict, error_config: bool = False):  # v1.2.9 更正backup_config参数类型。
        """备份当前的配置文件。"""
        if backup_config != Application.CONFIG_TEMPLATE:  # v1.2.9 修复比较变量错误的问题。
            backup_path = gen_backup_config(old_path=self.config_path,
                                            absolute_backup_dir=Application.ABSOLUTE_BACKUP_DIR,
                                            error_config=error_config)
            console.log(f'原来的配置文件已备份至"{backup_path}"', style='green')
        else:
            console.log('配置文件与模板文件完全一致,无需备份。')

    def load_config(self, error_config: bool = False) -> dict:
        """加载一次当前的配置文件,并附带合法性验证、缺失参数的检测以及各种异常时的处理措施。"""
        config: dict = Application.CONFIG_TEMPLATE.copy()
        try:
            if not os.path.exists(self.config_path):
                with open(file=self.config_path, mode='w', encoding='UTF-8') as f:
                    yaml.dump(Application.CONFIG_TEMPLATE, f, Dumper=CustomDumper)
                console.log('未找到配置文件,已生成新的模板文件...')
            with open(self.config_path, 'r') as f:
                config = yaml.safe_load(f)  # v1.1.4 加入对每个字段的完整性检测。
            config = self._check_params(config)  # 检查所有字段是否完整,modified代表是否有修改记录(只记录缺少的)
        except UnicodeDecodeError as e:  # v1.1.3 加入配置文件路径是中文或特殊字符时的错误提示,由于nuitka打包的性质决定,
            # 中文路径无法被打包好的二进制文件识别,故在配置文件时无论是链接路径还是媒体保存路径都请使用英文命名。
            error_config: bool = True
            log.warning(
                f'读取配置文件遇到编码错误,可能保存路径中包含中文或特殊字符的文件夹。已生成新的模板文件...原因:"{e}"')
            self.backup_config(config, error_config=error_config)
        except Exception as e:
            error_config: bool = True
            console.print('「注意」链接路径和保存路径不能有引号!', style='red')
            log.warning(f'检测到无效或损坏的配置文件。已生成新的模板文件...原因:"{e}"')
            self.backup_config(config, error_config=error_config)
        finally:
            if config is None:
                log.warning('检测到空的配置文件。已生成新的模板文件...')
                config: dict = Application.CONFIG_TEMPLATE.copy()
            if error_config:  # 如果遇到报错或者全部参数都是空的。
                return config
            # v1.1.4 加入是否重新编辑配置文件的引导。保证配置文件没有缺少任何字段,否则不询问。
            elif not self.modified and config != Application.CONFIG_TEMPLATE:
                while True:
                    try:
                        question = console.input(
                            '检测到已配置完成的配置文件,是否需要重新配置?(之前的配置文件将为你备份到当前目录下) - 「y|n」(默认n):').strip().lower()
                        if question == 'y':
                            config: dict = Application.CONFIG_TEMPLATE.copy()
                            backup_path: str = gen_backup_config(old_path=self.config_path,
                                                                 absolute_backup_dir=Application.ABSOLUTE_BACKUP_DIR)
                            console.log(
                                f'原来的配置文件已备份至"{backup_path}"', style='green')
                            self.get_last_history_record()  # 更新到上次填写的记录。
                            break
                        elif question == 'n' or question == '':
                            break
                        else:
                            log.warning(f'意外的参数:"{question}",支持的参数 - 「y|n」(默认n)')
                    except KeyboardInterrupt:
                        self._keyboard_interrupt()
            return config

    def save_config(self):
        """保存配置文件。"""
        with open(self.config_path, 'w') as f:
            yaml.dump(self._config, f)

    def _check_params(self, config: dict, history=False):
        """检查配置文件的参数是否完整。"""
        # 如果 config 为 None，初始化为一个空字典。
        if config is None:
            config = {}

        def add_missing_keys(target, template, log_message):
            """添加缺失的配置文件参数。"""
            for key, value in template.items():
                if key not in target:
                    target[key] = value
                    if not history:
                        console.log(log_message.format(key))
                        self.modified = True
                        self.record_flag = True

        def remove_extra_keys(target, template, log_message):
            """删除多余的配置文件参数。"""
            keys_to_remove: list = [key for key in target.keys() if key not in template]
            for key in keys_to_remove:
                target.pop(key)
                if not history:
                    console.log(log_message.format(key))
                    self.record_flag = True

        # 处理父级参数。
        add_missing_keys(target=config, template=Application.CONFIG_TEMPLATE, log_message='"{}"不在配置文件中,已添加。')
        # 特殊处理 proxy 参数。
        if 'proxy' in config:
            proxy_template = Application.CONFIG_TEMPLATE['proxy']
            proxy_config = config['proxy']

            # 确保 proxy_config 是字典。
            if not isinstance(proxy_config, dict):
                proxy_config: dict = {}
                config['proxy'] = proxy_config

            add_missing_keys(proxy_config, proxy_template, '"{}"不在proxy配置中,已添加。')
            remove_extra_keys(proxy_config, proxy_template, '"{}"不在proxy模板中,已删除。')

        # 删除父级模板中没有的字段。
        remove_extra_keys(config, Application.CONFIG_TEMPLATE, '"{}"不在模板中,已删除。')

        return config

    def _is_proxy_input(self, config: dict):
        """检测代理配置是否需要用户输入。"""
        result = False
        basic_truth_table: list = []
        advance_account_truth_table: list = []
        if config.get('enable_proxy') is False:  # 检测打开了代理但是代理配置错误。
            return False
        for _ in config.items():
            if _[0] in ['scheme', 'port', 'hostname']:
                basic_truth_table.append(_[1])
            if _[0] in ['username', 'password']:
                advance_account_truth_table.append(_[1])
        if all(basic_truth_table) is False:
            console.print('请配置代理!', style=self._stdio_style('config_proxy'))
            result = True
        if any(advance_account_truth_table) and all(advance_account_truth_table) is False:
            log.warning('代理账号或密码未输入!')
            result = True
        return result

    def _keyboard_interrupt(self):
        """处理配置文件交互时,当已配置了任意部分时的用户键盘中断。"""
        new_line = True
        try:
            if self.record_flag:
                print('\n')
                while True:
                    question = console.input('「退出提示」是否需要保存当前已填写的参数? - 「y|n」:').strip().lower()
                    if question == 'y':
                        console.log('配置已保存!')
                        self.save_config()
                        break
                    elif question == 'n':
                        console.log('不保存当前填写参数。')
                        break
                    else:
                        log.warning(f'意外的参数:"{question}",支持的参数 - 「y|n」')
            else:
                exit()
        except KeyboardInterrupt:
            new_line = False
            print('\n')
            console.log('用户放弃保存,手动终止配置参数。')
        finally:
            if new_line is True:
                print('\n')
                console.log('用户手动终止配置参数。')
            self.ctrl_c()
            exit()

    def _find_history_config(self):
        """找到历史配置文件。"""
        if not self.history_timestamp:
            return {}
        if not self.difference_timestamp:
            return {}
        try:
            min_key: int = min(self.difference_timestamp.keys())
            min_diff_timestamp: str = self.difference_timestamp.get(min_key)
            min_config_file: str = self.history_timestamp.get(min_diff_timestamp)
            if not min_config_file:
                return {}
            last_config_file = os.path.join(Application.ABSOLUTE_BACKUP_DIR, min_config_file)  # 拼接文件路径。
            with open(file=last_config_file, mode='r', encoding='UTF-8') as f:
                config = yaml.safe_load(f)
            last_record = self._check_params(config, history=True)  # v1.1.6修复读取历史如果缺失字段使得flag置True。

            if last_record == Application.CONFIG_TEMPLATE:
                # 从字典中删除当前文件。
                self.history_timestamp.pop(min_diff_timestamp, None)
                self.difference_timestamp.pop(min_key, None)
                # 递归调用。
                return self._find_history_config()
            else:
                return last_record
        except Exception as _:
            return {}

    def get_last_history_record(self):
        """获取最近一次保存的历史配置文件。"""
        # 首先判断是否存在目录文件。
        try:
            res: list = os.listdir(Application.ABSOLUTE_BACKUP_DIR)
        except FileNotFoundError:
            return
        except Exception as e:
            log.error(f'读取历史文件时发生错误,原因:"{e}"')
            return
        file_start: str = 'history_'
        file_end: str = '_config.yaml'

        now_timestamp = datetime.datetime.now().timestamp()  # 获取当前的时间戳。
        if res:
            for i in res:  # 找出离当前时间最近的配置文件。
                try:
                    if i.startswith(file_start) and i.endswith(file_end):
                        format_date_str = i.replace(file_start, '').replace(file_end, '').replace('_', ' ')
                        to_datetime_obj = datetime.datetime.strptime(format_date_str, '%Y-%m-%d %H-%M-%S')
                        timestamp = to_datetime_obj.timestamp()
                        self.history_timestamp[timestamp] = i
                except ValueError:
                    pass
                except Exception as _:
                    pass
            for i in self.history_timestamp.keys():
                self.difference_timestamp[now_timestamp - i] = i
            if self.history_timestamp:  # 如果有符合条件的历史配置文件。
                self.last_record = self._find_history_config()

        else:
            return

    def config_guide(self):
        """引导用户以交互式的方式修改、保存配置文件。"""
        # input user to input necessary configurations
        # v1.1.0 更替api_id和api_hash位置,与telegram申请的api位置对应以免输错。
        undefined = '无'
        _api_id = self._config.get('api_id')
        _api_hash = self._config.get('api_hash')
        _links = self._config.get('links')
        _save_path = self._config.get('save_path')
        _max_download_task = self._config.get('max_download_task')
        _download_type = self._config.get('download_type')
        _proxy = self._config.get('proxy')

        def get_api_id(_last_record):
            while True:
                try:
                    api_id = console.input(
                        f'请输入「api_id」上一次的记录是:「{_last_record if _last_record else undefined}」:').strip()
                    if api_id == '' and _last_record is not None:
                        api_id = _last_record
                    if Validator.is_valid_api_id(api_id):
                        self._config['api_id'] = api_id
                        console.print(f'已设置「api_id」为:「{api_id}」', style=self._stdio_style('api_id'))
                        self.record_flag = True
                        break
                except KeyboardInterrupt:
                    self._keyboard_interrupt()

        def get_api_hash(_last_record, _valid_length):
            while True:
                try:
                    api_hash = console.input(
                        f'请输入「api_hash」上一次的记录是:「{_last_record if _last_record else undefined}」:').strip().lower()
                    if api_hash == '' and _last_record is not None:
                        api_hash = _last_record
                    if Validator.is_valid_api_hash(api_hash, _valid_length):
                        self._config['api_hash'] = api_hash
                        console.print(f'已设置「api_hash」为:「{api_hash}」', style=self._stdio_style('api_hash'))
                        self.record_flag = True
                        break
                    else:
                        log.warning(f'意外的参数:"{api_hash}",不是一个「{_valid_length}位」的「值」!请重新输入!')
                except KeyboardInterrupt:
                    self._keyboard_interrupt()

        def get_links(_last_record, _valid_format):
            # 输入需要下载的媒体链接文件路径,确保文件存在。
            links_file = None
            while True:
                try:
                    links_file = console.input(
                        f'请输入需要下载的媒体链接的「完整路径」。上一次的记录是:「{_last_record if _last_record else undefined}」'
                        f'格式 - 「{_valid_format}」:').strip()
                    if links_file == '' and _last_record is not None:
                        links_file = _last_record
                    if Validator.is_valid_links_file(links_file, _valid_format):
                        self._config['links'] = links_file
                        console.print(f'已设置「links」为:「{links_file}」', style=self._stdio_style('links'))
                        self.record_flag = True
                        break
                    elif not os.path.normpath(links_file).endswith('.txt'):
                        log.warning(f'意外的参数:"{links_file}",文件路径必须以「{_valid_format}」结尾,请重新输入!')
                    else:
                        log.warning(
                            f'意外的参数:"{links_file}",文件路径必须以「{_valid_format}」结尾,并且「必须存在」,请重新输入!')
                except KeyboardInterrupt:
                    self._keyboard_interrupt()
                except Exception as _e:
                    log.error(f'意外的参数:"{links_file}",请重新输入!原因:"{_e}"')

        def get_save_path(_last_record):
            # 输入媒体保存路径,确保是一个有效的目录路径。
            while True:
                try:
                    save_path = console.input(
                        f'请输入媒体「保存路径」。上一次的记录是:「{_last_record if _last_record else undefined}」:').strip()
                    if save_path == '' and _last_record is not None:
                        save_path = _last_record
                    if Validator.is_valid_save_path(save_path):
                        self._config['save_path'] = save_path
                        console.print(f'已设置「save_path」为:「{save_path}」', style=self._stdio_style('save_path'))
                        self.record_flag = True
                        break
                    elif os.path.isfile(save_path):
                        log.warning(f'意外的参数:"{save_path}",指定的路径是一个文件并非目录,请重新输入!')
                    else:
                        log.warning(f'意外的参数:"{save_path}",指定的路径无效或不是一个目录,请重新输入!')
                except KeyboardInterrupt:
                    self._keyboard_interrupt()

        def get_max_download_task(_last_record):
            # 输入最大下载任务数,确保是一个整数且不超过特定限制。
            while True:
                try:
                    max_tasks = console.input(
                        f'请输入「最大下载任务数」。上一次的记录是:「{_last_record if _last_record else undefined}」'
                        f'非会员建议默认{"(默认3)" if _last_record is None else ""}:').strip()
                    if max_tasks == '' and _last_record is not None:
                        max_tasks = _last_record
                    if max_tasks == '':
                        max_tasks = 3
                    if Validator.is_valid_max_download_task(max_tasks):
                        self._config['max_download_task'] = int(max_tasks)
                        console.print(f'已设置「max_download_task」为:「{max_tasks}」',
                                      style=self._stdio_style('max_download_task'))
                        self.record_flag = True
                        break
                    else:
                        log.warning(f'意外的参数:"{max_tasks}",任务数必须是「正整数」,请重新输入!')
                except KeyboardInterrupt:
                    self._keyboard_interrupt()
                except Exception as _e:
                    log.error(f'意外的错误,原因:"{_e}"')

        def get_is_shutdown(_last_record, _valid_format):
            if _last_record:
                _last_record = 'y'
            elif _last_record is False:
                _last_record = 'n'
            else:
                _last_record = undefined
            _style: str = self._stdio_style('is_shutdown')
            while True:
                try:
                    question = console.input(
                        f'下载完成后是否「自动关机」。上一次的记录是:「{_last_record}」 - 「{_valid_format}」'
                        f'{"(默认n)" if _last_record == undefined else ""}:').strip().lower()
                    if question == '' and _last_record != undefined:
                        if _last_record == 'y':
                            self._config['is_shutdown'] = True
                            console.print(f'已设置「is_shutdown」为:「{_last_record}」,下载完成后将自动关机!',
                                          style=_style)
                            self.record_flag = True
                            break
                        elif _last_record == 'n':
                            self._config['is_shutdown'] = False
                            console.print(f'已设置「is_shutdown」为:「{_last_record}」', style=_style)
                            self.record_flag = True
                            break
                    elif question == 'y':
                        self._config['is_shutdown'] = True
                        console.print(f'已设置「is_shutdown」为:「{question}」,下载完成后将自动关机!', style='Pink1')
                        self.record_flag = True
                        break
                    elif question == 'n' or question == '':
                        self._config['is_shutdown'] = False
                        console.print(f'已设置「is_shutdown」为:「n」', style=_style)
                        self.record_flag = True
                        break
                    else:
                        log.warning(f'意外的参数:"{question}",支持的参数 - 「{_valid_format}」')
                except KeyboardInterrupt:
                    self._keyboard_interrupt()
                except Exception as _e:
                    log.error(f'意外的错误,原因:"{_e}"')
                    break

        def get_download_type(_last_record: list):
            def _set_dtype(_dtype) -> list:
                i_dtype = int(_dtype)  # 因为终端输入是字符串，这里需要转换为整数。
                if i_dtype == 1:
                    return [DownloadType.video.text]
                elif i_dtype == 2:
                    return [DownloadType.photo.text]
                elif i_dtype == 3:
                    return [DownloadType.video.text, DownloadType.photo.text]

            if _last_record is not None:
                if isinstance(_last_record, list):
                    res: dict = self._get_dtype(download_dtype=_last_record)
                    if len(res) == 1:
                        _last_record = None
                    elif res.get('video') and res.get('photo') is False:
                        _last_record = 1
                    elif res.get('video') is False and res.get('photo'):
                        _last_record = 2
                    elif res.get('video') and res.get('photo'):
                        _last_record = 3
                else:
                    _last_record = None
            while True:
                try:
                    download_type = console.input(
                        f'输入需要下载的「媒体类型」。上一次的记录是:「{_last_record if _last_record else undefined}」'
                        f'格式 - 「1.视频 2.图片 3.视频和图片」{"(默认3)" if _last_record is None else ""}:').strip()
                    if download_type == '' and _last_record is not None:
                        download_type = _last_record
                    if download_type == '':
                        download_type = 3
                    if Validator.is_valid_download_type(download_type):
                        self._config['download_type'] = _set_dtype(_dtype=download_type)
                        console.print(f'已设置「download_type」为:「{download_type}」',
                                      style=self._stdio_style('download_type'))
                        self.record_flag = True
                        break
                    else:
                        log.warning(f'意外的参数:"{download_type}",支持的参数 - 「1或2或3」')
                except KeyboardInterrupt:
                    self._keyboard_interrupt()

        if any([
            not _api_id,
            not _api_hash,
            not _links,
            not _save_path,
            not _max_download_task,
            not _download_type,
            not _proxy,
            not (self._config.get('proxy') or {}).get('enable_proxy', False),
            not (self._config.get('proxy') or {}).get('hostname', False),
            not (self._config.get('proxy') or {}).get('is_notice', False),
            not (self._config.get('proxy') or {}).get('username', False),
            not (self._config.get('proxy') or {}).get('password', False),
            not (self._config.get('proxy') or {}).get('scheme', False)
        ]):
            console.print('「注意」直接回车代表使用上次的记录。', style='red')

        if not _api_id:
            last_record = self.last_record.get('api_id')
            get_api_id(_last_record=last_record)
        if not _api_hash:
            last_record = self.last_record.get('api_hash')
            get_api_hash(_last_record=last_record, _valid_length=32)
        if not _links:
            last_record = self.last_record.get('links')
            get_links(_last_record=last_record, _valid_format='.txt')
        if not _save_path:
            last_record = self.last_record.get('save_path')
            get_save_path(_last_record=last_record)
        if not _max_download_task:
            last_record = self.last_record.get('max_download_task') if self.last_record.get(
                'max_download_task') else None
            get_max_download_task(_last_record=last_record)
        if not _download_type:
            last_record = self.last_record.get('download_type') if self.last_record.get(
                'download_type') else None
            get_download_type(_last_record=last_record)
        # v1.1.6 下载完成自动关机。
        last_record = self.last_record.get('is_shutdown')
        get_is_shutdown(_last_record=last_record, _valid_format='y|n')

        proxy_config: dict = self._config.get('proxy', {})  # 读取proxy字段得到字典。
        # v1.1.4 移除self._check_proxy_params(proxy_config)改用全字段检测  # 检查代理字典字段是否完整并自动补全保存。
        enable_proxy = self._config.get('proxy') or {}.get('enable_proxy', False)
        proxy_record = self.last_record.get('proxy') if self.last_record.get('proxy') else {}

        def get_proxy_info(_scheme, _hostname, _port):
            if _scheme is None:
                _scheme = proxy_record.get('scheme', '未知')
            if _hostname is None:
                _hostname = proxy_record.get('hostname', '未知')
            if _port is None:
                _port = proxy_record.get('port', '未知')
            return _scheme, _hostname, _port

        if proxy_config.get('is_notice') is True or proxy_config.get('is_notice') is None:  # 如果打开了通知或第一次配置。
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
            valid_format: str = 'y|n'

            try:
                while True:  # 询问是否开启代理。
                    enable_proxy = console.input(
                        f'是否需要使用「代理」。上一次的记录是:「{ep_notice}」'
                        f'格式 - 「{valid_format}」{"(默认n)" if ep_notice == undefined else ""}:').strip().lower()
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
                        console.print(f'已设置「enable_proxy」为:「{enable_proxy}」',
                                      style=self._stdio_style('enable_proxy'))
                        self.record_flag = True
                        break
                    else:
                        log.error(f'意外的参数:"{enable_proxy}",请输入有效参数!支持的参数 - 「{valid_format}」!')
                while True:
                    # 是否记住选项。
                    is_notice = console.input(
                        f'下次是否「不再询问使用代理」。上一次的记录是:「{in_notice}」'
                        f'格式 - 「{valid_format}」{("(默认n)" if in_notice == undefined else "")}:').strip().lower()
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
                        console.print(f'已设置「is_notice」为:「{is_notice}」', style=self._stdio_style('is_notice'))
                        self.record_flag = True
                        break
                    else:
                        log.error(f'意外的参数:"{is_notice}",请输入有效参数!支持的参数 - 「{valid_format}」!')

            except KeyboardInterrupt:
                self._keyboard_interrupt()

        if enable_proxy == 'y' or enable_proxy is True:
            scheme = None
            hostname = None
            port = None
            if self._is_proxy_input(proxy_config):
                valid_port = '0~65535'
                # 输入代理类型。
                if not proxy_config['scheme']:
                    valid_format: list = ['http', 'socks4', 'socks5']
                    last_record = proxy_record.get('scheme')
                    while True:
                        try:
                            scheme = console.input(
                                f'请输入「代理类型」。上一次的记录是:「{last_record if last_record else undefined}」'
                                f'格式 - 「{"|".join(valid_format)}」:').strip().lower()
                            if scheme == '' and last_record is not None:
                                scheme = last_record
                            if Validator.is_valid_scheme(scheme, valid_format):
                                proxy_config['scheme'] = scheme
                                self.record_flag = True
                                console.print(f'已设置「scheme」为:「{scheme}」', style=self._stdio_style('scheme'))
                                break
                            else:
                                log.warning(
                                    f'意外的参数:"{scheme}",请输入有效的代理类型!支持的参数 - 「{"|".join(valid_format)}」!')
                        except KeyboardInterrupt:
                            self._keyboard_interrupt()
                if not proxy_config.get('hostname'):
                    valid_format: str = 'x.x.x.x'
                    last_record = self.last_record.get('proxy', {}).get('hostname')
                    while True:
                        scheme, _, __ = get_proxy_info(scheme, None, None)
                        # 输入代理IP地址。
                        try:
                            hostname = console.input(
                                f'请输入代理类型为:"{scheme}"的「ip地址」。上一次的记录是:「{last_record if last_record else undefined}」'
                                f'格式 - 「{valid_format}」:').strip()
                            if hostname == '' and last_record is not None:
                                hostname = last_record
                            if Validator.is_valid_hostname(hostname):
                                proxy_config['hostname'] = hostname
                                self.record_flag = True
                                console.print(f'已设置「hostname」为:「{hostname}」', style=self._stdio_style('hostname'))
                                break
                        except ValueError:
                            log.warning(
                                f'"{hostname}"不是一个「ip地址」,请输入有效的ipv4地址!支持的参数 - 「{valid_format}」!')
                        except KeyboardInterrupt:
                            self._keyboard_interrupt()
                if not proxy_config.get('port'):
                    last_record = self.last_record.get('proxy', {}).get('port')
                    # 输入代理端口。
                    while True:
                        try:  # hostname，scheme可能出现None
                            scheme, hostname, __ = get_proxy_info(scheme, hostname, None)
                            port = console.input(
                                f'请输入ip地址为:"{hostname}",代理类型为:"{scheme}"的「代理端口」。'
                                f'上一次的记录是:「{last_record if last_record else undefined}」'
                                f'格式 - 「{valid_port}」:').strip()
                            if port == '' and last_record is not None:
                                port = last_record
                            if Validator.is_valid_port(port):
                                proxy_config['port'] = int(port)
                                self.record_flag = True
                                console.print(f'已设置「port」为:「{port}」', style=self._stdio_style('port'))
                                break
                            else:
                                log.warning(f'意外的参数:"{port}",端口号必须在「{valid_port}」之间!')
                        except ValueError:
                            log.warning(f'意外的参数:"{port}",请输入一个有效的整数!支持的参数 - 「{valid_port}」')
                        except KeyboardInterrupt:
                            self._keyboard_interrupt()
                        except Exception as e:
                            log.error(f'意外的错误,原因:"{e}"')
                if not all([proxy_config.get('username'), proxy_config.get('password')]):
                    # 是否需要认证。
                    style = self._stdio_style('proxy_authentication')
                    valid_format: str = 'y|n'
                    while True:
                        try:
                            is_proxy = console.input(f'代理是否需要「认证」? - 「{valid_format}」(默认n):').strip().lower()
                            if is_proxy == 'y':
                                try:
                                    proxy_config['username'] = console.input('请输入「用户名」:').strip()
                                    self.record_flag = True
                                    proxy_config['password'] = console.input('请输入「密码」:').strip()
                                    self.record_flag = True
                                    console.print(f'已设置为:「代理需要认证」', style=style)
                                except KeyboardInterrupt:
                                    self._keyboard_interrupt()
                                finally:
                                    break
                            elif is_proxy == 'n' or is_proxy == '':
                                proxy_config['username'] = None
                                proxy_config['password'] = None
                                console.print(f'已设置为:「代理不需要认证」', style=style)
                                break
                            else:
                                log.warning(f'意外的参数:"{is_proxy}",支持的参数 - 「{valid_format}」!')
                        except KeyboardInterrupt:
                            self._keyboard_interrupt()
        self.save_config()
        return


class PanelTable:
    def __init__(self, title: str, header: tuple, data: list, styles: dict = None):
        self.table = Table(title=title, highlight=True)
        self.table.title_style = Style(color='white', bold=True)
        # 添加列。
        for i, col in enumerate(header):
            style = styles.get(col, {}) if styles else {}
            self.table.add_column(col, **style)

        # 添加数据行。
        for row in data:
            self.table.add_row(*map(str, row))  # 确保数据项是字符串类型，防止类型错误。

    def print_meta(self):
        console.print(self.table, justify='center')


class MetaData:
    @staticmethod
    def check_run_env() -> bool:  # 检测是windows平台下控制台运行还是IDE运行。
        try:
            from ctypes import windll  # v1.2.9 避免非Windows平台运行时报错。
            return windll.kernel32.SetConsoleTextAttribute(windll.kernel32.GetStdHandle(-0xb), 0x7)
        except ImportError:  # v1.2.9 抛出错误代表非Windows平台。
            return True

    @staticmethod
    def pay():
        if MetaData.check_run_env():  # 是终端才打印,生产环境会报错。
            try:
                console.print(
                    MetaData._qr_terminal_str(
                        'wxp://f2f0g8lKGhzEsr0rwtKWTTB2gQzs9Xg9g31aBvlpbILowMTa5SAMMEwn0JH1VEf2TGbS'),
                    justify='center')
                console.print(
                    GradientColor.gen_gradient_text(text='欢迎微信扫码支持作者!',
                                                    gradient_color=GradientColor.yellow_to_green),
                    justify='center')
            except Exception as _:
                pass

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

    @staticmethod
    def suitable_units_display(number: int) -> str:
        result: dict = MetaData._determine_suitable_units(number)
        return result.get('number') + result.get('unit')

    @staticmethod
    def _determine_suitable_units(number, unit=None) -> dict:
        units = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
        if unit in units:
            index = units.index(unit)
            value = number / (1024 ** index)
            return {'number': float('{:.2f}'.format(value)), 'unit': unit}
        else:
            values = [number]
            for i in range(len(units) - 1):
                if values[i] >= 1024:
                    values.append(values[i] / 1024)
                else:
                    break
            return {'number': '{:.2f}'.format(values[-1]), 'unit': units[len(values) - 1]}

    @staticmethod
    def print_helper():
        markdown = Markdown(readme)
        console.print(markdown)

    @staticmethod
    def get_platform() -> dict:
        return {'system': platform.system()}

    @staticmethod
    def _qr_terminal_str(str_obj: str, version: int = 1, render: callable = QrcodeRender.render_2by1) -> str:
        qr = qrcode.QRCode(version)
        qr.add_data(str_obj)
        qr.make()
        qr_row: int = len(qr.modules) + 2
        qr_col: int = len(qr.modules[0]) + 2
        qr_map: list = [[False for _ in range(qr_col)] for _ in range(qr_row)]
        for row_id, row in enumerate(qr.modules):
            for col_id, pixel in enumerate(row):
                qr_map[row_id + 1][col_id + 1] = pixel
        return render(qr_map)

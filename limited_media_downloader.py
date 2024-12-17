# coding=UTF-8
# Author:Gentlesprite
# Software:PyCharm
# Time:2023/10/3 1:00:03
# File:limited_media_downloader.py
import asyncio
from functools import wraps
from rich.progress import Progress, TextColumn, BarColumn, TimeRemainingColumn, TransferSpeedColumn
from module import Set, Dict, Any
from module import SessionRevoked, AuthKeyUnregistered, SessionExpired, MsgIdInvalid, UsernameInvalid
from module import TelegramRestrictedMediaDownloaderClient
from module import console, log
from module import mimetypes
from module import os
from module import pyrogram
from module import SOFTWARE_FULL_NAME
from module.app import Application, PanelTable, MetaData
from module.enum_define import LinkType, DownloadStatus, DownloadType, KeyWorld, GradientColor
from module.process_path import split_path, is_file_duplicate, validate_title, truncate_filename, \
    safe_delete, move_to_download_path
from module.pyrogram_extension import get_extension


class RestrictedMediaDownloader:
    downloading = DownloadStatus.translate(DownloadStatus.downloading.text)
    success_download = DownloadStatus.translate(DownloadStatus.success.text)
    failure_download = DownloadStatus.translate(DownloadStatus.failure.text)
    skip_download = DownloadStatus.translate(DownloadStatus.skip.text)
    keyword_link = KeyWorld.translate(KeyWorld.link.text, True)
    keyword_link_type = KeyWorld.translate(KeyWorld.link_type.text, True)
    keyword_id = KeyWorld.translate(KeyWorld.id.text, True)
    keyword_size = KeyWorld.translate(KeyWorld.size.text, True)
    keyword_link_status = KeyWorld.translate(KeyWorld.status.text, True)
    keyword_file = KeyWorld.translate(KeyWorld.file.text, True)
    keyword_error_size = KeyWorld.translate(KeyWorld.error_size.text, True)
    keyword_actual_size = KeyWorld.translate(KeyWorld.actual_size.text, True)
    keyword_already_exist = KeyWorld.translate(KeyWorld.already_exist.text, True)
    keyword_chanel = KeyWorld.translate(KeyWorld.chanel.text, True)
    keyword_type = KeyWorld.translate(KeyWorld.type.text, True)
    keyword_download_task_error = KeyWorld.translate(KeyWorld.download_task_error.text, True)
    event = asyncio.Event()

    def __init__(self):
        MetaData.print_helper()
        self.queue = asyncio.Queue()
        self.app = Application()
        self.app.config_guide()
        self.config: dict = self.app.config.copy()
        self.temp_folder: str = self.app.TEMP_FOLDER
        self.record_dtype: set = set()
        self.api_hash: str = ''
        self.api_id: str = ''
        self.download_type: list = []
        self.is_shutdown: bool = False
        self.links: str = ''
        self.max_download_task: int = 3
        self.proxy: dict = {}
        self.enable_proxy: dict or None = None
        self.save_path: str = ''
        self._get_config()
        self.workdir = os.path.join(os.getcwd(), 'sessions')
        os.makedirs(self.workdir, exist_ok=True)
        self.client = TelegramRestrictedMediaDownloaderClient(name=SOFTWARE_FULL_NAME.replace(' ', ''),
                                                              api_id=self.api_id,
                                                              api_hash=self.api_hash,
                                                              proxy=self.enable_proxy,
                                                              workdir=self.workdir)
        self.current_task_num: int = 0
        self.max_retry_count: int = 3
        self.skip_video, self.skip_photo = set(), set()
        self.success_video, self.success_photo = set(), set()
        self.failure_video, self.failure_photo = set(), set()
        self.failure_link: dict = {}  # v1.1.2
        self.progress = Progress(TextColumn("[bold blue]{task.fields[filename]}", justify="right"),
                                 BarColumn(bar_width=40),
                                 "[progress.percentage]{task.percentage:>3.1f}%",
                                 "•",
                                 '[bold green]{task.fields[info]}',
                                 "•",
                                 TransferSpeedColumn(),
                                 "•",
                                 TimeRemainingColumn(),
                                 console=console
                                 )

    def _get_config(self):
        self.api_hash = self.config.get('api_hash')
        self.api_id = self.config.get('api_id')
        self.download_type: list = self.config.get('download_type')
        self.is_shutdown: bool = self.config.get('is_shutdown')
        self.links: str = self.config.get('links')
        self.max_download_task: int = self.config.get('max_download_task')
        self.proxy = self.config.get('proxy', {})
        self.enable_proxy = self.proxy if self.proxy.get('enable_proxy') else None
        self.save_path: str = self.config.get('save_path')
        if self.download_type is not None and (
                DownloadType.video.text in self.download_type or DownloadType.photo.text in self.download_type):
            self.record_dtype.update(self.download_type)  # v1.2.4 修复特定情况结束后不显示表格问题
            self.download_type.append(DownloadType.document.text)
        else:
            self.download_type: list = DownloadType.support_type()
            self.record_dtype: set = {DownloadType.video.text,
                                      DownloadType.photo.text}  # v1.2.4 修复此处报错问题v1.2.3此处有致命错误
            console.log(f'已使用默认下载类型:3.视频和图片。')

    def _print_config_table(self):
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
            # 展示链接内容表格
            with open(file=self.links, mode='r', encoding='UTF-8') as _:
                res = [content.strip() for content in _.readlines()]
            format_res: list = []
            for i in enumerate(res, start=1):
                format_res.append(list(i))
            link_table = PanelTable(title='链接内容', header=('编号', '链接'),
                                    data=format_res)
            link_table.print_meta()
        except FileNotFoundError:  # v1.1.3 用户错误填写路径提示
            log.error(f'读取"{self.links}"时出错。')
        except Exception as e:
            log.error(f'读取"{self.links}"时出错,原因:"{e}"')
        try:
            _dtype = self.download_type.copy()  # 浅拷贝赋值给_dtype,避免传入函数后改变原数据
            data = [[DownloadType.translate(DownloadType.video.text),
                     self.app.get_dtype(_dtype).get('video')],
                    [DownloadType.translate(DownloadType.photo.text),
                     self.app.get_dtype(_dtype).get('photo')]]
            download_type_table = PanelTable(title='下载类型', header=('类型', '是否下载'), data=data)
            download_type_table.print_meta()

        except Exception as e:
            log.error(f'读取"{self.links}"时出错,原因:"{e}"')

    def _media_counter(func):
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
            if self.failure_video and self.success_video:
                for i in self.failure_video:
                    if i in self.success_video:
                        self.failure_video.remove(i)
            return res

        return wrapper

    @_media_counter
    def _guess_file_type(self, file_name, status):
        result = ''
        file_type, _ = mimetypes.guess_type(file_name)
        if file_type is not None:
            file_main_type: str = file_type.split('/')[0]
            if file_main_type == 'image':
                result = DownloadType.photo
            elif file_main_type == 'video':
                result = DownloadType.video
        return result, status

    def _get_temp_path(self, message: pyrogram.types.Message,
                       dtype: DownloadType.text) -> str:
        file_name = None
        os.makedirs(self.temp_folder, exist_ok=True)

        def _process_video(msg_obj: pyrogram.types, _dtype: DownloadType.text):
            _meta_obj = getattr(msg_obj, _dtype)
            _file_name = '{} - {}.{}'.format(
                getattr(msg_obj, 'id'),
                os.path.splitext(getattr(_meta_obj, 'file_name'))[0],
                get_extension(file_id=_meta_obj.file_id, mime_type=getattr(_meta_obj, 'mime_type'), dot=False)
            )
            _file_name = os.path.join(self.temp_folder, validate_title(_file_name))
            return _file_name

        def _process_photo(msg_obj: pyrogram.types, _dtype: DownloadType.text):
            _meta_obj = getattr(msg_obj, _dtype)
            extension = 'unknown'
            if _dtype == DownloadType.photo.text:
                extension = get_extension(file_id=_meta_obj.file_id, mime_type='image',
                                          dot=False)
            elif _dtype == DownloadType.document.text:
                extension = get_extension(file_id=_meta_obj.file_id, mime_type=getattr(_meta_obj, 'mime_type'),
                                          dot=False)
            _file_name = '{} - {}.{}'.format(
                getattr(msg_obj, 'id'),
                _meta_obj.file_unique_id,
                extension
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

    def _check_download_finish(self, sever_size: int, download_path: str, save_directory: str) -> bool:
        local_size: int = os.path.getsize(download_path)
        format_local_size: str = MetaData.suitable_units_display(local_size)
        format_sever_size: str = MetaData.suitable_units_display(sever_size)
        save_path: str = os.path.join(save_directory, split_path(download_path).get('file_name'))
        if sever_size == local_size:
            result: dict = move_to_download_path(temp_save_path=download_path, save_path=save_directory).get('e_code')
            console.log(result) if result is not None else 0
            console.log(
                f'{self.keyword_file}:"{save_path}",'
                f'{self.keyword_size}:{format_local_size},'
                f'{self.keyword_type}:{DownloadType.translate(self._guess_file_type(file_name=download_path, status=DownloadStatus.success)[0].text)},'
                f'{self.keyword_link_status}:{DownloadStatus.translate(DownloadStatus.success.text)}。',
            )
            return True
        else:
            console.log(
                f'{self.keyword_file}:"{save_path}",'
                f'{self.keyword_error_size}:{format_local_size},'
                f'{self.keyword_actual_size}:{format_sever_size},'
                f'{self.keyword_type}:{DownloadType.translate(self._guess_file_type(file_name=download_path, status=DownloadStatus.failure)[0].text)},'
                f'{self.keyword_link_status}:{self.failure_download}。')
            os.remove(download_path)
            return False

    async def _extract_link_content(self, msg_link):
        comment_message = []
        is_comment = False
        if '?single&comment' in msg_link:  # v1.1.0修复讨论组中附带?single时不下载的问题
            is_comment = True
        if '?single' in msg_link:  # todo 如果用户只想下载组中的其一
            msg_link = msg_link.split('?single')[0]
        if '?comment' in msg_link:  # 链接中包含?comment表示用户需要同时下载评论中的媒体
            msg_link = msg_link.split('?comment')[0]
            is_comment = True
        msg_id = int(msg_link.split('/')[-1])
        if 't.me/c/' in msg_link:
            if 't.me/b/' in msg_link:
                chat_name = str(msg_link.split('/')[-2])
            else:
                chat_name = int('-100' + str(msg_link.split('/')[-2]))  # 得到频道的id
        else:
            chat_name = msg_link.split('/')[-2]  # 频道的名字

        if is_comment:
            # 如果用户需要同时下载媒体下面的评论,把评论中的所有信息放入列表一起返回
            async for comment in self.client.get_discussion_replies(chat_name, msg_id):
                comment_message.append(comment)

        return chat_name, msg_id, comment_message

    @staticmethod
    async def _is_group(message) -> Any:
        try:
            return True, await message.get_media_group()
        except ValueError as e:
            return False, None if str(e) == "The message doesn't belong to a media group" else 0
            # v1.0.4 修改单文件无法下载问题return False, [] if str(e) == "The message doesn't belong to a media group" else 0
        except AttributeError:
            return None, None

    def _get_media_meta(self, message, dtype) -> dict:
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

    def _get_valid_dtype(self, message) -> Dict[str, bool]:
        valid_dtype = next((i for i in DownloadType.support_type() if getattr(message, i, None)),
                           None)  # 判断该链接是否为视频或图片,文档
        is_document_type_valid = None
        # 当媒体文件是文档形式的,需要根据配置需求将视频和图片过滤出来
        if getattr(message, 'document'):
            mime_type = message.document.mime_type  # 获取document的mime_type
            # 只下载视频的情况
            if DownloadType.video.text in self.download_type and DownloadType.photo.text not in self.download_type:
                if 'video' in mime_type:
                    is_document_type_valid = True  # 允许下载视频
                elif 'image' in mime_type:
                    is_document_type_valid = False  # 跳过下载图片
            # 只下载图片的情况
            elif DownloadType.photo.text in self.download_type and DownloadType.video.text not in self.download_type:
                if 'video' in mime_type:
                    is_document_type_valid = False  # 跳过下载视频
                elif 'image' in mime_type:
                    is_document_type_valid = True  # 允许下载图片
            else:
                is_document_type_valid = True
        else:
            is_document_type_valid = True
        return {'valid_dtype': valid_dtype,
                'is_document_type_valid': is_document_type_valid}

    async def _add_task(self, msg_link, message, retry_count=0):
        _task = None
        valid_dtype, is_document_type_valid = self._get_valid_dtype(message).values()
        if valid_dtype in self.download_type and is_document_type_valid:
            # 如果是匹配到的消息类型就创建任务
            while self.current_task_num >= self.max_download_task:  # v1.0.7 增加下载任务数限制
                await self.event.wait()
                self.event.clear()
            temp_save_path, sever_size, file_name, local_file_path, format_file_size = self._get_media_meta(
                message=message,
                dtype=valid_dtype).values()
            if is_file_duplicate(local_file_path=local_file_path,
                                 sever_size=sever_size):  # 检测是否存在
                console.log(f'{self.keyword_file}:"{file_name}",'
                            f'{self.keyword_size}:{format_file_size},'
                            f'{self.keyword_type}:{DownloadType.translate(self._guess_file_type(file_name=file_name, status=DownloadStatus.skip)[0].text)},'
                            f'{self.keyword_already_exist}:"{local_file_path}",'
                            f'{self.keyword_link_status}:{self.skip_download}。', style='yellow')
            else:
                console.log(f'{self.keyword_file}:"{file_name}",'
                            f'{self.keyword_size}:{format_file_size},'
                            f'{self.keyword_type}:{DownloadType.translate(self._guess_file_type(file_name=file_name, status=DownloadStatus.downloading)[0].text)},'
                            f'{self.keyword_link_status}:{self.downloading}。')
                task_id = self.progress.add_task(description='',
                                                 filename=file_name,
                                                 info=f'0.00B/{MetaData.suitable_units_display(sever_size)}',
                                                 total=sever_size)
                _task = asyncio.create_task(
                    self.client.download_media(message=message,
                                               progress_args=(self.progress, task_id),
                                               progress=self._download_bar,
                                               file_name=temp_save_path))
                console.log(f'[当前任务数]:{self.current_task_num}。', justify='right')

                def call(_future):
                    self.current_task_num -= 1
                    if self._check_download_finish(sever_size=sever_size,
                                                   download_path=temp_save_path,
                                                   save_directory=self.save_path):
                        console.log(f'[当前任务数]:{self.current_task_num}。', justify='right')
                        self.event.set()
                    else:
                        if retry_count < self.max_retry_count:
                            console.log(
                                f'[重新下载]:"{file_name}",[重试次数]:{retry_count + 1}/{self.max_retry_count}。')
                            self.queue.put_nowait((msg_link, message, retry_count + 1))
                        else:
                            _error = f'(达到最大重试次数:{self.max_retry_count}次)。'
                            console.log(f'{self.keyword_file}:"{file_name}"',
                                        f'{self.keyword_size}:{format_file_size},'
                                        f'{self.keyword_type}:{DownloadType.translate(self._guess_file_type(file_name=temp_save_path, status=DownloadStatus.failure)[0].text)},'
                                        f'{self.keyword_link_status}:{self.failure_download}'
                                        f'{_error}')
                            self.failure_link[msg_link] = _error.replace('。', '')
                            self.event.set()

                _task.add_done_callback(lambda _future: call(_future))
        if _task:
            self.queue.put_nowait(_task)

    async def _get_download_task(self,
                                 msg_link: str = None,
                                 message=None,
                                 retry_count=0):

        if msg_link:
            try:
                chat_name, msg_id, is_download_comment = await self._extract_link_content(msg_link)
                msg = await self.client.get_messages(chat_name, msg_id)  # 该消息的信息
                res, group = await self._is_group(msg)
                if res or is_download_comment:  # 组或评论区
                    try:  # v1.1.2解决当group返回None时出现comment无法下载的问题
                        group.extend(is_download_comment) if is_download_comment else 0
                    except AttributeError:
                        if is_download_comment and group is None:
                            group = []
                            group.extend(is_download_comment)
                    link_type = LinkType.comment.text if is_download_comment else LinkType.group.text
                    log.info(
                        f'{self.keyword_chanel}:"{chat_name}",'  # 频道名
                        f'{self.keyword_link}:"{msg_link}",'  # 链接
                        f'{self.keyword_link_type}:{LinkType.translate(link_type)}。')  # 链接类型
                    [await self._add_task(msg_link, msg_group, retry_count) for msg_group in group]

                elif res is False and group is None:  # 单文件
                    link_type = LinkType.single.text
                    console.log(
                        f'{self.keyword_chanel}:"{chat_name}",'  # 频道名
                        f'{self.keyword_link}:"{msg_link}",'  # 链接
                        f'{self.keyword_link_type}:{LinkType.translate(link_type)}。')  # 链接类型
                    await self._add_task(msg_link, msg, retry_count)
                elif res is None and group is None:
                    error = '消息不存在,频道已解散或未在频道中'
                    self.failure_link[msg_link] = error
                    log.warning(
                        f'{self.keyword_link}:"{msg_link}"{error},{self.skip_download}。')
                elif res is None and group == 0:
                    log.error(f'读取"{msg_link}"时出现未知错误,{self.skip_download}。')
            except UnicodeEncodeError as e:
                error = '频道标题存在特殊字符,请移步终端下载'
                self.failure_link[msg_link] = e
                log.error(f'{self.keyword_link}:"{msg_link}"{error},原因:"{e}"')
            except MsgIdInvalid as e:
                self.failure_link[msg_link] = e
                log.error(f'{self.keyword_link}:"{msg_link}"消息不存在,可能已删除,{self.skip_download}。原因:"{e}"')
            except UsernameInvalid as e:
                self.failure_link[msg_link] = e
                log.error(
                    f'{self.keyword_link}:"{msg_link}"频道用户名无效,该链接的频道用户名可能已更改或频道已解散,{self.skip_download}。原因:"{e}"')
            except Exception as e:
                self.failure_link[msg_link] = e
                log.error(
                    f'{self.keyword_link}:"{msg_link}"未收录到的错误,{self.skip_download}。原因:"{e}"')
        else:
            await self._add_task(msg_link, message, retry_count)

    @staticmethod
    def _download_bar(current, total, progress, task_id):
        progress.update(task_id,
                        completed=current,
                        info=f'{MetaData.suitable_units_display(current)}/{MetaData.suitable_units_display(total)}',
                        total=total)

    def _process_links(self, links: str) -> Set[str]:
        start_content: str = 'https://t.me/'
        msg_link_set: set = set()
        if isinstance(links, str):
            if links.endswith('.txt') and os.path.isfile(links):
                with open(file=links, mode='r', encoding='UTF-8') as _:
                    for link in [content.strip() for content in _.readlines()]:
                        if link.startswith(start_content):
                            msg_link_set.add(link)
                        else:
                            log.warning(f'"{link}"是一个非法链接,{self.keyword_link_status}:{self.skip_download}。')
            elif not os.path.isfile(links):  # v1.1.3 优化非文件时的提示和逻辑
                if links.endswith('.txt'):
                    log.error(f'文件"{links}"不存在。')
                else:
                    log.error(f'"{links}"是一个目录或其他未知内容,并非.txt结尾的文本文件,请更正配置文件后重试。')
        if len(msg_link_set) > 0:
            return msg_link_set
        else:
            console.log('没有找到有效链接,程序已退出。')
            exit()

    async def _download_media_from_links(self):
        await self.client.start()
        self.progress.start()  # v1.1.8修复登录输入手机号不显示文本问题
        # 将初始任务添加到队列中
        for link in self._process_links(links=self.links):
            await self._get_download_task(msg_link=link)

        # 处理队列中的任务
        while not self.queue.empty():
            task = await self.queue.get()
            if isinstance(task, tuple):
                msg_link, message, retry_count = task
                await self._get_download_task(msg_link=msg_link, message=message, retry_count=retry_count)
            else:
                await task
            self.queue.task_done()

        # 等待所有任务完成
        await self.queue.join()

    def run(self):
        record_error = False

        def _print_media_table():
            header = ('种类&状态', '成功下载', '失败下载', '跳过下载', '合计')
            if DownloadType.document.text in self.download_type:
                self.download_type.remove(DownloadType.document.text)
            total_video = len(self.success_video) + len(self.failure_video) + len(self.skip_video)
            total_photo = len(self.success_photo) + len(self.failure_photo) + len(self.skip_photo)
            if len(self.record_dtype) == 1:
                _compare_dtype: list = list(self.record_dtype)[0]
                if _compare_dtype == 'video':  # 只有视频的情况
                    video_table = PanelTable(title='视频下载统计',
                                             header=header,
                                             data=[
                                                 [DownloadType.translate(DownloadType.video.text),
                                                  len(self.success_video),
                                                  len(self.failure_video),
                                                  len(self.skip_video),
                                                  total_video],
                                                 ['合计', len(self.success_video),
                                                  len(self.failure_video),
                                                  len(self.skip_video),
                                                  total_video]
                                             ]
                                             )
                    video_table.print_meta()
                if _compare_dtype == 'photo':  # 只有图片的情况
                    total_photo = len(self.success_photo) + len(self.failure_photo) + len(self.skip_photo)
                    photo_table = PanelTable(title='图片下载统计',
                                             header=header,
                                             data=[
                                                 [DownloadType.translate(DownloadType.photo.text),
                                                  len(self.success_photo),
                                                  len(self.failure_photo),
                                                  len(self.skip_photo),
                                                  total_photo],
                                                 ['合计', len(self.success_photo),
                                                  len(self.failure_photo),
                                                  len(self.skip_photo),
                                                  total_photo]
                                             ]
                                             )
                    photo_table.print_meta()
            elif len(self.record_dtype) == 2:
                media_table = PanelTable(title='媒体下载统计',
                                         header=header,
                                         data=[
                                             [DownloadType.translate(DownloadType.video.text), len(self.success_video),
                                              len(self.failure_video),
                                              len(self.skip_video),
                                              total_video],
                                             [DownloadType.translate(DownloadType.photo.text), len(self.success_photo),
                                              len(self.failure_photo),
                                              len(self.skip_photo),
                                              total_photo],
                                             ['合计', len(self.success_video) + len(self.success_photo),
                                              len(self.failure_video) + len(self.failure_photo),
                                              len(self.skip_video) + len(self.skip_photo), total_video + total_photo]
                                         ])
                media_table.print_meta()

        def _print_failure_table():
            format_failure_info: list = []
            for index, (key, value) in enumerate(self.failure_link.items(), start=1):
                format_failure_info.append([index, key, value])
            failure_link_table = PanelTable(title='失败链接统计',
                                            header=('编号', '链接', '原因'),
                                            data=format_failure_info)
            failure_link_table.print_meta()

        def _process_shutdown():
            if self.is_shutdown:
                self.app.shutdown_task(second=60)

        try:
            MetaData.print_meta()
            self._print_config_table()
            self.client.run(self._download_media_from_links())
        except (SessionRevoked, AuthKeyUnregistered, SessionExpired, ConnectionError):
            res = safe_delete(file_path=os.path.join(self.app.DIR_NAME, 'sessions'))
            if res:
                log.warning('账号已失效请重新登录!')
            else:
                log.error('账号已失效请手动删除软件目录下的sessions文件并重新登录!')
        except KeyboardInterrupt:
            self.progress.stop()
            console.log('用户手动终止下载任务。')
        except Exception as e:
            self.progress.stop()
            record_error = True
            log.exception(msg=f'运行出错,原因:"{e}"', exc_info=True)
        finally:
            if self.client.is_connected:
                self.client.stop()
            self.progress.stop()
            if not record_error:
                _print_media_table()
                _print_failure_table() if self.failure_link else 0  # v1.1.2 增加下载失败的链接统计,但如果没有失败的链接将不会显示
                MetaData.pay()
                _process_shutdown()
            os.system('pause')

# coding=UTF-8
# Author:LZY/我不是盘神
# Software:PyCharm
# Time:2023/10/3 1:00:03
# File:limited_media_downloader
import shutil
import asyncio
from functools import wraps
from rich.progress import Progress, TextColumn, BarColumn, TimeRemainingColumn, TransferSpeedColumn
import module
from module import os
from module import mimetypes
from module import pyrogram
from module import console, logger
from module import List, Any
from module.app import Application, PanelTable, pay, print_meta
from module.unit import suitable_units_display
from module.pyrogram_extension import get_extension
from module.enum_define import LinkType, DownloadStatus, DownloadType, KeyWorld
from module.process_path import split_path, is_folder_empty, is_file_duplicate, validate_title, truncate_filename


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
    APP_NAME = 'TelegramRestrictedMediaDownloader'
    event = asyncio.Event()

    def __init__(self):
        self.app = Application()
        self.app.config_guide()
        self.temp_folder: str = self.app.TEMP_FOLDER
        self.save_path: str = self.app.config.get('save_path')
        self.max_download_task: int = self.app.config.get('max_download_task')
        self.links: List[str] or str = self.app.config.get('links')
        os.makedirs(os.path.join(os.getcwd(), 'sessions'), exist_ok=True)
        self.client = module.TelegramRestrictedMediaDownloaderClient(name=self.APP_NAME,
                                                                     api_id=self.app.config.get('api_id'),
                                                                     api_hash=self.app.config.get('api_hash'),
                                                                     proxy=self.app.config.get(
                                                                         'proxy', {}) if self.app.config.get('proxy',
                                                                                                             {}).get(
                                                                         'enable_proxy') else None,
                                                                     workdir=os.path.join(os.getcwd(), 'sessions'))
        self.current_task_num = 0
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

    def _config_table(self):
        try:
            if self.app.config.get('proxy', {}).get('enable_proxy'):
                logger.info('当前正在使用代理!')
                proxy_key: list = []
                proxy_value: list = []
                for i in self.app.config.get('proxy').items():
                    if i[0] not in ['username', 'password']:
                        key, value = i
                        proxy_key.append(key)
                        proxy_value.append(value)
                proxy_table = PanelTable(title='代理配置', header=tuple(proxy_key), data=[proxy_value])
                proxy_table.print_meta(style='yellow')
            else:
                logger.info('当前没有使用代理!')
        except Exception as e:
            try:
                logger.info(self.app.config)
            except Exception as _:
                logger.error(f'配置信息打印错误!原因"{_}"')
            logger.error(f'表格打印错误!原因"{e}"')
        file_path = self.app.config.get('links')
        try:
            # 展示链接内容表格
            with open(file=file_path, mode='r', encoding='UTF-8') as _:
                res = [content.strip() for content in _.readlines()]
            format_res: list = []
            for i in enumerate(res, start=1):
                format_res.append(list(i))
            link_table = PanelTable(title='链接内容', header=('编号', '链接'),
                                    data=format_res)
            link_table.print_meta(style='#279947')
        except FileNotFoundError:  # v1.1.3 用户错误填写路径提示
            logger.error(f'读取"{file_path}"时出错。')
        except Exception as e:
            logger.error(f'读取"{file_path}"时出错,原因:{e}')

    @staticmethod
    def _move_to_download_path(temp_save_path: str, save_path: str):
        os.makedirs(save_path, exist_ok=True)
        if os.path.isdir(save_path):
            shutil.move(temp_save_path, save_path)
        else:
            console.print(f'"{save_path}"不是一个目录,已将文件下载到默认目录。')
            if is_folder_empty(save_path):
                os.rmdir(save_path)
            save_path = os.path.join(os.getcwd(), 'downloads')
            os.makedirs(save_path, exist_ok=True)
            shutil.move(temp_save_path, save_path)

    def _recorder(func):
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
            return res

        return wrapper

    @_recorder
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
                       mime_type: DownloadType) -> str:
        file_name = None
        os.makedirs(self.temp_folder, exist_ok=True)
        if mime_type == DownloadType.video.text:
            file_name = "{} - {}.{}".format(
                message.id,
                os.path.splitext(f'{message.video.file_name}')[0],
                get_extension(file_id=message.video.file_id, mime_type=DownloadType.video.text, dot=False)
            )
            file_name = os.path.join(self.temp_folder, validate_title(file_name))
        elif mime_type == DownloadType.photo.text:
            file_name = "{} - {}.{}".format(
                message.id,
                message.photo.file_unique_id,
                get_extension(file_id=message.photo.file_id, mime_type=DownloadType.photo.text, dot=False)
            )
            file_name = os.path.join(self.temp_folder, validate_title(file_name))
        return truncate_filename(file_name)

    def _check_download_finish(self, sever_size: int, download_path: str, save_directory: str):
        local_size: int = os.path.getsize(download_path)
        format_local_size, format_sever_size = suitable_units_display(local_size), suitable_units_display(sever_size)
        save_path: str = os.path.join(save_directory, split_path(download_path)[1])
        if sever_size == local_size:
            # TODO: 根据下载的文件判断其类型对其精准分类计数:视频个数,图片个数
            self._move_to_download_path(temp_save_path=download_path, save_path=save_directory)
            console.print(
                f'{self.keyword_file}:"{save_path}",'
                f'{self.keyword_size}:{format_local_size},'
                f'{self.keyword_type}:{DownloadType.translate(self._guess_file_type(file_name=download_path, status=DownloadStatus.success)[0].text)},'
                f'{self.keyword_link_status}:{DownloadStatus.translate(DownloadStatus.success.text)}。',
            )  # todo 后续加入下载任务链接的文件名,解决组或者讨论组下载的媒体链接都是一样的,但是媒体有多个,导致不好区分的问题

        else:
            console.print(f'{self.keyword_file}:"{save_path}",'
                          f'{self.keyword_error_size}:{format_local_size},'
                          f'{self.keyword_actual_size}:{format_sever_size},'
                          f'{self.keyword_type}:{DownloadType.translate(self._guess_file_type(file_name=download_path, status=DownloadStatus.failure)[0].text)},'
                          f'{self.keyword_link_status}:{self.failure_download}')
            os.remove(download_path)

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

    async def _get_download_task(self, msg_link: str) -> set:
        tasks = set()

        async def add_task(message):
            # 判断消息类型
            _task = None
            mime_type = next((i for i in DownloadType.support_type() if getattr(message, i, None)), None)
            # 如果是匹配到的消息类型就创建任务
            if mime_type:
                _temp_save_path: str = self._get_temp_path(message, mime_type)
                while self.current_task_num >= self.max_download_task:  # v1.0.7 增加下载任务数限制
                    await self.event.wait()
                    self.event.clear()
                sever_meta = getattr(message, mime_type)
                sever_size: int = getattr(sever_meta, 'file_size')
                file_name: str = split_path(_temp_save_path)[1]
                local_file_path: str = os.path.join(self.save_path, file_name)
                format_file_size: str = suitable_units_display(sever_size)
                if is_file_duplicate(local_file_path=local_file_path,
                                     sever_size=sever_size):  # 检测是否存在
                    console.print(f'{self.keyword_file}:"{file_name}",'
                                  f'{self.keyword_size}:{format_file_size},'
                                  f'{self.keyword_type}:{DownloadType.translate(self._guess_file_type(file_name=file_name, status=DownloadStatus.skip)[0].text)},'
                                  f'{self.keyword_already_exist}:"{local_file_path}",'
                                  f'{self.keyword_link_status}:{self.skip_download}。', style='yellow')
                else:
                    console.print(f'{self.keyword_file}:"{file_name}",'
                                  f'{self.keyword_size}:{format_file_size},'
                                  f'{self.keyword_type}:{DownloadType.translate(self._guess_file_type(file_name=file_name, status=DownloadStatus.downloading)[0].text)},'
                                  f'{self.keyword_link_status}:{self.downloading}。')
                    task_id = self.progress.add_task(description='',
                                                     filename=file_name,
                                                     info=f'0.00B/{suitable_units_display(sever_size)}',
                                                     total=sever_size)
                    _task = asyncio.create_task(
                        self.client.download_media(message=message,
                                                   progress_args=(self.progress, task_id),
                                                   progress=self._download_bar,
                                                   file_name=_temp_save_path))
                    console.print(f'当前任务数:{self.current_task_num}。')

                    def call(future):
                        self.current_task_num -= 1
                        if future.exception() is not None:
                            console.print(f'{self.keyword_download_task_error}:"{future.exception()}"')
                            # todo 后续可能实现下载出错重试功能
                        else:
                            self._check_download_finish(sever_size=sever_size, download_path=_temp_save_path,
                                                        save_directory=self.save_path)
                        console.print(f'当前任务数:{self.current_task_num}。')
                        self.event.set()

                    _task.add_done_callback(lambda future: call(future))
            tasks.add(_task) if _task else 0

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
                console.print(
                    f'{self.keyword_chanel}:"{chat_name}",'  # 频道名
                    f'{self.keyword_link}:"{msg_link}",'  # 链接
                    f'{self.keyword_link_type}:{LinkType.translate(link_type)}。')  # 链接类型
                [await add_task(msg_group) for msg_group in group]

            elif res is False and group is None:  # 单文件
                link_type = LinkType.single.text
                console.print(
                    f'{self.keyword_chanel}:"{chat_name}",'  # 频道名
                    f'{self.keyword_link}:"{msg_link}",'  # 链接
                    f'{self.keyword_link_type}:{LinkType.translate(link_type)}。')  # 链接类型
                await add_task(msg)
            elif res is None and group is None:
                error = '消息不存在,频道已解散或未在频道中'
                self.failure_link[msg_link] = error
                console.print(
                    f'{self.keyword_link}:"{msg_link}"{error},{self.skip_download}。', style='yellow')
            elif res is None and group == 0:
                console.print(f'读取"{msg_link}"时出现未知错误,{self.skip_download}。', style='red')
        except UnicodeEncodeError as e:
            error = '频道标题存在特殊字符,请移步终端下载'
            self.failure_link[msg_link] = e
            console.print(f'{self.keyword_link}:"{msg_link}"{error},原因:"{e}"', style='red')
        except pyrogram.errors.exceptions.bad_request_400.MsgIdInvalid as e:
            self.failure_link[msg_link] = e
            console.print(f'{self.keyword_link}:"{msg_link}"消息不存在,可能已删除,{self.skip_download}。原因:"{e}"',
                          style='red')
        except Exception as e:
            self.failure_link[msg_link] = e
            # todo 测试倘若频道中确实不存在的报错,进行判断提示,非该错误则不提示,并且注意区分错误在于未加入频道,还是已加入频道视频被删了,甚至是频道直接解散了
            console.print(
                f'{self.keyword_link}:"{msg_link}"消息不存在,频道已解散或未在频道中,{self.skip_download}。原因:"{e}"',
                style='red')
        finally:
            return tasks

    @staticmethod
    def _download_bar(current, total, progress, task_id):
        progress.update(task_id,
                        completed=current,
                        info=f'{suitable_units_display(current)}/{suitable_units_display(total)}',
                        total=total)

    def _process_links(self, links: str) -> List[str]:
        start_content: str = 'https://t.me/'
        msg_link_list: list = []
        if isinstance(links, str):
            if links.endswith('.txt') and os.path.isfile(links):
                with open(file=links, mode='r', encoding='UTF-8') as _:
                    for link in [content.strip() for content in _.readlines()]:
                        if link.startswith(start_content):
                            msg_link_list.append(link)
                        else:
                            logger.warning(f'"{link}"是一个非法链接,{self.keyword_link_status}:{self.skip_download}。')
            elif not os.path.isfile(links):  # v1.1.3 优化非文件时的提示和逻辑
                if links.endswith('.txt'):
                    logger.error(f'文件"{links}"不存在。')
                else:
                    logger.error(f'"{links}"是一个目录或其他未知内容,并非.txt结尾的文本文件,请更正配置文件后重试。')
        if len(msg_link_list) > 0:
            return msg_link_list
        else:
            logger.info('没有找到有效链接,程序已退出。')
            exit()

    async def _download_media_from_links(self):
        await self.client.start()
        self.progress.start()  # v1.1.8修复登录输入手机号不显示文本问题
        tasks = set()
        for link in self._process_links(links=self.links):
            res = await self._get_download_task(msg_link=link)
            tasks.update(res)  # v1.1.0修复同一链接若第一次未下载完整,在第二次补全时,任务创建了但不等待该下载完成就结束程序,导致下载不完全的的致命性问题
        await asyncio.gather(*tasks)

    def run(self):
        record_error = False
        try:
            print_meta()
            self._config_table()
            self.client.run(self._download_media_from_links())
        except Exception as e:
            self.progress.stop()
            record_error = True
            self._config_table()
            logger.error(
                f'运行出错,原因:"{e}"')
            while True:
                question = console.input('是否重新配置文件?(之前的配置文件将为你备份到当前目录下) - 「y|n」:').lower()
                if question == 'y':
                    self.app.backup_config(self.app.config_path)  # 备份config.yaml
                    self.app.history_record()  # 更新到上次填写的记录
                    self.app.config = self.app.CONFIG_TEMPLATE  # 恢复为默认配置开始重新配置
                    self.app.save_config()
                    rmd = RestrictedMediaDownloader()
                    rmd.run()
                    break
                elif question == 'n':
                    logger.info('程序已退出。')
                    exit(0)
        except KeyboardInterrupt:
            self.progress.stop()
            logger.info('用户手动终止下载任务。')
        finally:
            self.progress.stop()
            if not record_error:
                total_video = len(self.success_video) + len(self.failure_video) + len(self.skip_video)
                total_photo = len(self.success_photo) + len(self.failure_photo) + len(self.skip_photo)
                media_table = PanelTable(title='媒体下载统计',
                                         header=('种类&状态', '成功下载', '失败下载', '跳过下载', '合计'),
                                         data=[
                                             ["视频", len(self.success_video), len(self.failure_video),
                                              len(self.skip_video),
                                              total_video],
                                             ["图片", len(self.success_photo), len(self.failure_photo),
                                              len(self.skip_photo),
                                              total_photo],
                                             ["合计", len(self.success_video) + len(self.success_photo),
                                              len(self.failure_video) + len(self.failure_photo),
                                              len(self.skip_video) + len(self.skip_photo), total_video + total_photo]
                                         ])
                media_table.print_meta(style='#06a3d7')
                if self.failure_link:  # v1.1.2 增加下载失败的链接统计,但如果没有失败的链接将不会显示
                    format_failure_info: list = []
                    for index, (key, value) in enumerate(self.failure_link.items(), start=1):
                        format_failure_info.append([index, key, value])
                    failure_link_table = PanelTable(title='失败链接统计',
                                                    header=('编号', '链接', '原因'),
                                                    data=format_failure_info)
                    failure_link_table.print_meta(style='#e53e30')
                pay()
                if self.app.config.get('is_shutdown'):
                    self.app.shutdown_task(second=60)
                else:
                    os.system('pause')

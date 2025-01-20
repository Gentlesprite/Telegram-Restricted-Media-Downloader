# coding=UTF-8
# Author:Gentlesprite
# Software:PyCharm
# Time:2023/10/3 1:00:03
# File:downloader.py
import os
import asyncio

from pyrogram.errors.exceptions.bad_request_400 import MsgIdInvalid, UsernameInvalid
from pyrogram.errors.exceptions.unauthorized_401 import SessionRevoked, AuthKeyUnregistered, SessionExpired

from typing import Set, Any
from module import console, log
from module.app import Application, MetaData
from module.process_path import is_file_duplicate, safe_delete
from module.enum_define import LinkType, DownloadStatus, DownloadType
from module.enum_define import downloading, failure_download, skip_download, keyword_link, keyword_link_type, \
    keyword_size, keyword_link_status, keyword_file, keyword_already_exist, keyword_chanel, keyword_type


class TelegramRestrictedMediaDownloader:

    def __init__(self):
        MetaData.print_helper()
        self.event = asyncio.Event()
        self.queue = asyncio.Queue()
        self.app = Application()
        self.client = self.app.build_client()

    async def _extract_link_content(self, msg_link):
        comment_message = []
        is_comment = False
        if '?single&comment' in msg_link:  # v1.1.0修复讨论组中附带?single时不下载的问题，
            is_comment = True
        if '?single' in msg_link:  # todo 如果用户只想下载组中的其一
            msg_link = msg_link.split('?single')[0]
        if '?comment' in msg_link:  # 链接中包含?comment表示用户需要同时下载评论中的媒体。
            msg_link = msg_link.split('?comment')[0]
            is_comment = True
        msg_id = int(msg_link.split('/')[-1])
        if 't.me/c/' in msg_link:
            if 't.me/b/' in msg_link:
                chat_name = str(msg_link.split('/')[-2])
            else:
                chat_name = int('-100' + str(msg_link.split('/')[-2]))  # 得到频道的id。
        else:
            chat_name = msg_link.split('/')[-2]  # 频道的名字。

        if is_comment:
            # 如果用户需要同时下载媒体下面的评论,把评论中的所有信息放入列表一起返回。
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

    async def _add_task(self, msg_link, message, retry_count=0):
        _task = None
        valid_dtype, is_document_type_valid = self.app.get_valid_dtype(message).values()
        if valid_dtype in self.app.download_type and is_document_type_valid:
            # 如果是匹配到的消息类型就创建任务。
            while self.app.current_task_num >= self.app.max_download_task:  # v1.0.7 增加下载任务数限制。
                await self.event.wait()
                self.event.clear()
            temp_save_path, sever_size, file_name, local_file_path, format_file_size = self.app.get_media_meta(
                message=message,
                dtype=valid_dtype).values()
            if is_file_duplicate(local_file_path=local_file_path,
                                 sever_size=sever_size):  # 检测是否存在。
                if retry_count == 0:  # v1.2.9 下载失败时,不再重复打印已存在的文件信息。
                    console.log(f'{keyword_file}:"{file_name}",'
                                f'{keyword_size}:{format_file_size},'
                                f'{keyword_type}:{DownloadType.translate(self.app.guess_file_type(file_name=file_name, status=DownloadStatus.skip)[0].text)},'
                                f'{keyword_already_exist}:"{local_file_path}",'
                                f'{keyword_link_status}:{skip_download}。', style='yellow')
            else:
                console.log(f'{keyword_file}:"{file_name}",'
                            f'{keyword_size}:{format_file_size},'
                            f'{keyword_type}:{DownloadType.translate(self.app.guess_file_type(file_name=file_name, status=DownloadStatus.downloading)[0].text)},'
                            f'{keyword_link_status}:{downloading}。')
                task_id = self.app.progress.add_task(description='',
                                                     filename=file_name,
                                                     info=f'0.00B/{MetaData.suitable_units_display(sever_size)}',
                                                     total=sever_size)
                _task = asyncio.create_task(
                    self.client.download_media(message=message,
                                               progress_args=(self.app.progress, task_id),
                                               progress=self.app.download_bar,
                                               file_name=temp_save_path))
                console.log(f'[当前任务数]:{self.app.current_task_num}。', justify='right')

                def call(_future):
                    self.app.current_task_num -= 1
                    if self.app.check_download_finish(sever_size=sever_size,
                                                      download_path=temp_save_path,
                                                      save_directory=self.app.save_path):
                        console.log(f'[当前任务数]:{self.app.current_task_num}。', justify='right')
                        self.event.set()
                    else:
                        self.app.progress.remove_task(task_id=task_id)  # v1.2.9 更正下载失败时,删除下载失败的进度条。
                        if retry_count < self.app.max_retry_count:
                            console.log(
                                f'[重新下载]:"{file_name}",[重试次数]:{retry_count + 1}/{self.app.max_retry_count}。')
                            self.queue.put_nowait((msg_link, message, retry_count + 1))
                        else:
                            _error = f'(达到最大重试次数:{self.app.max_retry_count}次)。'
                            console.log(f'{keyword_file}:"{file_name}"',
                                        f'{keyword_size}:{format_file_size},'
                                        f'{keyword_type}:{DownloadType.translate(self.app.guess_file_type(file_name=temp_save_path, status=DownloadStatus.failure)[0].text)},'
                                        f'{keyword_link_status}:{failure_download}'
                                        f'{_error}')
                            self.app.failure_link[msg_link] = _error.replace('。', '')
                            self.event.set()

                _task.add_done_callback(lambda _future: call(_future))
        self.queue.put_nowait(_task) if _task else 0

    async def _get_download_task(self,
                                 msg_link: str = None,
                                 message=None,
                                 retry_count=0):

        if msg_link:
            try:
                chat_name, msg_id, is_download_comment = await self._extract_link_content(msg_link)
                msg = await self.client.get_messages(chat_name, msg_id)  # 该消息的信息。
                res, group = await self._is_group(msg)
                if res or is_download_comment:  # 组或评论区。
                    try:  # v1.1.2解决当group返回None时出现comment无法下载的问题。
                        group.extend(is_download_comment) if is_download_comment else 0
                    except AttributeError:
                        if is_download_comment and group is None:
                            group = []
                            group.extend(is_download_comment)
                    link_type = LinkType.comment.text if is_download_comment else LinkType.group.text
                    log.info(
                        f'{keyword_chanel}:"{chat_name}",'  # 频道名。
                        f'{keyword_link}:"{msg_link}",'  # 链接。
                        f'{keyword_link_type}:{LinkType.translate(link_type)}。')  # 链接类型。
                    [await self._add_task(msg_link, msg_group, retry_count) for msg_group in group]

                elif res is False and group is None:  # 单文件。
                    link_type = LinkType.single.text
                    console.log(
                        f'{keyword_chanel}:"{chat_name}",'  # 频道名。
                        f'{keyword_link}:"{msg_link}",'  # 链接。
                        f'{keyword_link_type}:{LinkType.translate(link_type)}。')  # 链接类型。
                    await self._add_task(msg_link, msg, retry_count)
                elif res is None and group is None:
                    error = '消息不存在,频道已解散或未在频道中'
                    self.app.failure_link[msg_link] = error
                    log.warning(
                        f'{keyword_link}:"{msg_link}"{error},{skip_download}。')
                elif res is None and group == 0:
                    log.error(f'读取"{msg_link}"时出现未知错误,{skip_download}。')
            except UnicodeEncodeError as e:
                error = '频道标题存在特殊字符,请移步终端下载'
                self.app.failure_link[msg_link] = e
                log.error(f'{keyword_link}:"{msg_link}"{error},原因:"{e}"')
            except MsgIdInvalid as e:
                self.app.failure_link[msg_link] = e
                log.error(f'{keyword_link}:"{msg_link}"消息不存在,可能已删除,{skip_download}。原因:"{e}"')
            except UsernameInvalid as e:
                self.app.failure_link[msg_link] = e
                log.error(
                    f'{keyword_link}:"{msg_link}"频道用户名无效,该链接的频道用户名可能已更改或频道已解散,{skip_download}。原因:"{e}"')
            except Exception as e:
                self.app.failure_link[msg_link] = e
                log.error(
                    f'{keyword_link}:"{msg_link}"未收录到的错误,{skip_download}。原因:"{e}"')
        else:
            await self._add_task(msg_link, message, retry_count)

    @staticmethod
    def _process_links(links: str) -> Set[str]:
        start_content: str = 'https://t.me/'
        msg_link_set: set = set()
        if isinstance(links, str):
            if links.endswith('.txt') and os.path.isfile(links):
                with open(file=links, mode='r', encoding='UTF-8') as _:
                    for link in [content.strip() for content in _.readlines()]:
                        if link.startswith(start_content):
                            msg_link_set.add(link)
                        else:
                            log.warning(f'"{link}"是一个非法链接,{keyword_link_status}:{skip_download}。')
            elif not os.path.isfile(links):  # v1.1.3 优化非文件时的提示和逻辑。
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
        self.app.progress.start()  # v1.1.8修复登录输入手机号不显示文本问题。
        # 将初始任务添加到队列中。
        for link in self._process_links(links=self.app.links):
            await self._get_download_task(msg_link=link)

        # 处理队列中的任务。
        while not self.queue.empty():
            task = await self.queue.get()
            if isinstance(task, tuple):
                msg_link, message, retry_count = task
                await self._get_download_task(msg_link=msg_link, message=message, retry_count=retry_count)
            else:
                await task
            self.queue.task_done()

        # 等待所有任务完成。
        await self.queue.join()

    def run(self):
        record_error: bool = False
        was_client_run: bool = False

        try:
            MetaData.print_meta()
            self.app.print_config_table()
            self.client.run(self._download_media_from_links())
            was_client_run = True
        except (SessionRevoked, AuthKeyUnregistered, SessionExpired, ConnectionError):
            res: bool = safe_delete(file_path=os.path.join(self.app.DIR_NAME, 'sessions'))
            record_error = True
            if res:
                log.warning('账号已失效请在关闭后,再次打开软件并重新登录!')
            else:
                log.error('账号已失效请手动删除软件目录下的sessions文件并重新登录!')
        except KeyboardInterrupt:
            self.app.progress.stop()
            console.log('用户手动终止下载任务。')
        except Exception as e:
            self.app.progress.stop()
            record_error = True
            log.exception(msg=f'运行出错,原因:"{e}"', exc_info=True)
        finally:
            if self.client.is_connected:
                was_client_run = True
                self.client.stop()
            self.app.progress.stop()
            if not record_error:
                self.app.print_media_table()
                self.app.print_failure_table() if self.app.failure_link else 0  # v1.1.2 增加下载失败的链接统计,但如果没有失败的链接将不会显示。
                MetaData.pay()
                self.app.process_shutdown() if was_client_run else 0  # v1.2.8如果并未打开客户端执行任何下载,则不执行关机。
            if self.app.platform == 'Windows':
                self.app.ctrl_c()
            else:
                console.input('请按「Enter」键继续. . .')

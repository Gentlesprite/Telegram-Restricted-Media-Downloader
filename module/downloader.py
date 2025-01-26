# coding=UTF-8
# Author:Gentlesprite
# Software:PyCharm
# Time:2023/10/3 1:00:03
# File:downloader.py
import os
import sys
import asyncio
from typing import Tuple

import pyrogram
from pyrogram.errors.exceptions.bad_request_400 import MsgIdInvalid, UsernameInvalid
from pyrogram.errors.exceptions.unauthorized_401 import SessionRevoked, AuthKeyUnregistered, SessionExpired

from module import console, log
from module.bot import Bot
from module.app import Application, MetaData
from module.process_path import is_file_duplicate, safe_delete
from module.enum_define import LinkType, DownloadStatus, DownloadType, KeyWord, Status


class TelegramRestrictedMediaDownloader(Bot):

    def __init__(self):
        super().__init__()
        MetaData.print_helper()
        self.event = asyncio.Event()
        self.queue = asyncio.Queue()
        self.app = Application()
        self.client = self.app.build_client()

    async def get_link_from_bot(self,
                                client: pyrogram.Client,
                                message: pyrogram.types.Message):
        await super().get_link_from_bot(client, message)
        if self.message is None:
            return
        else:
            links: set or None = self.__process_links(link=self.message)
            if links is None:
                console.log('没有找到有效链接。')
                return
            else:
                for link in links:
                    if link in self.app.complete_link:
                        log.warning(f'链接"{link}"已下载完成,请勿重复下载。')
                    else:
                        await self.__create_download_task(link)

    async def pay_callback(self, client: pyrogram.Client, callback: pyrogram.types.CallbackQuery):
        MetaData.pay()
        await super().pay_callback(client, callback)

    async def __extract_link_content(self, msg_link) -> Tuple[str, int, list]:
        comment_message = []
        is_comment = False
        if '?single&comment' in msg_link:  # v1.1.0修复讨论组中附带?single时不下载的问题，
            is_comment = True
        if '?single' in msg_link:  # todo 如果只想下载组中的其一。
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
    async def __is_group(message) -> Tuple[bool or None, bool or None]:
        try:
            return True, await message.get_media_group()
        except ValueError:
            return False, None  # v1.0.4 修改单文件无法下载问题。
        except AttributeError:
            return None, None

    def __listen_link_complete(self, msg_link, file_name) -> bool:
        self.app.link_info.get(msg_link).get('file_name').add(file_name)
        for i in self.app.link_info.items():
            link: str = i[0]
            info: dict = i[1]
            if link == msg_link:
                info['complete_num'] = len(info.get('file_name'))
        all_num: int = self.app.link_info.get(msg_link).get('member_num')
        complete_num: int = self.app.link_info.get(msg_link).get('complete_num')
        if all_num == complete_num:
            console.log(f'{KeyWord.LINK}:"{msg_link}",'
                        f'{KeyWord.STATUS}:{Status.SUCCESS}。')
            self.app.complete_link.add(msg_link)
            return True
        else:
            return False

    async def __add_task(self, msg_link, message, retry_count: int = 0) -> None:
        _task = None
        valid_dtype, is_document_type_valid = self.app.get_valid_dtype(message).values()
        if valid_dtype in self.app.download_type and is_document_type_valid:
            # 如果是匹配到的消息类型就创建任务。
            while self.app.current_task_num >= self.app.max_download_task:  # v1.0.7 增加下载任务数限制。
                await self.event.wait()
                self.event.clear()
            temp_file_path, sever_file_size, file_name, save_directory, format_file_size = self.app.get_media_meta(
                message=message,
                dtype=valid_dtype).values()
            if is_file_duplicate(save_directory=save_directory,
                                 sever_file_size=sever_file_size):  # 检测是否存在。
                if retry_count == 0:  # v1.2.9 下载失败时,不再重复打印已存在的文件信息。
                    console.log(f'{KeyWord.FILE}:"{file_name}",'
                                f'{KeyWord.SIZE}:{format_file_size},'
                                f'{KeyWord.TYPE}:{DownloadType.t(self.app.guess_file_type(file_name=file_name, status=DownloadStatus.skip)[0].text)},'
                                f'{KeyWord.ALREADY_EXIST}:"{save_directory}",'
                                f'{KeyWord.STATUS}:{Status.SKIP}。', style='yellow')
                self.__listen_link_complete(msg_link=msg_link, file_name=file_name)
            else:
                console.log(f'{KeyWord.FILE}:"{file_name}",'
                            f'{KeyWord.SIZE}:{format_file_size},'
                            f'{KeyWord.TYPE}:{DownloadType.t(self.app.guess_file_type(file_name=file_name, status=DownloadStatus.downloading)[0].text)},'
                            f'{KeyWord.STATUS}:{Status.DOWNLOADING}。')
                task_id = self.app.progress.add_task(description='',
                                                     filename=file_name,
                                                     info=f'0.00B/{format_file_size}',
                                                     total=sever_file_size)
                _task = asyncio.create_task(
                    self.client.download_media(message=message,
                                               progress_args=(self.app.progress, task_id),
                                               progress=self.app.download_bar,
                                               file_name=temp_file_path))
                console.log(f'[当前任务数]:{self.app.current_task_num}。', justify='right')

                def call(_future) -> None:
                    self.app.current_task_num -= 1
                    if self.app.check_download_finish(sever_file_size=sever_file_size,
                                                      temp_file_path=temp_file_path,
                                                      save_directory=self.app.save_directory,
                                                      with_move=True):
                        self.__listen_link_complete(msg_link=msg_link, file_name=file_name)
                        console.log(f'[当前任务数]:{self.app.current_task_num}。', justify='right')
                        self.app.progress.remove_task(task_id=task_id)
                        self.event.set()
                    else:
                        self.app.progress.remove_task(task_id=task_id)  # v1.2.9 更正下载失败时,删除下载失败的进度条。
                        if retry_count < self.app.max_retry_count:
                            console.log(
                                f'[重新下载]:"{file_name}",[重试次数]:{retry_count + 1}/{self.app.max_retry_count}。')
                            self.queue.put_nowait((msg_link, message, retry_count + 1))
                        else:
                            _error = f'(达到最大重试次数:{self.app.max_retry_count}次)。'
                            console.log(f'{KeyWord.FILE}:"{file_name}",'
                                        f'{KeyWord.SIZE}:{format_file_size},'
                                        f'{KeyWord.TYPE}:{DownloadType.t(self.app.guess_file_type(file_name=file_name, status=DownloadStatus.failure)[0].text)},'
                                        f'{KeyWord.STATUS}:{Status.FAILURE}'
                                        f'{_error}')
                            self.app.failure_link[msg_link] = _error.replace('。', '')
                            self.event.set()

                _task.add_done_callback(lambda _future: call(_future))
        self.queue.put_nowait(_task) if _task else None

    async def __create_download_task(self,
                                     msg_link: str = None,
                                     message=None,
                                     retry_count: int = 0) -> None:

        if msg_link:
            try:
                chat_name, msg_id, is_download_comment = await self.__extract_link_content(msg_link)
                msg = await self.client.get_messages(chat_name, msg_id)  # 该消息的信息。
                res, group = await self.__is_group(msg)
                if res or is_download_comment:  # 组或评论区。
                    try:  # v1.1.2解决当group返回None时出现comment无法下载的问题。
                        group.extend(is_download_comment) if is_download_comment else None
                    except AttributeError:
                        if is_download_comment and group is None:
                            group = []
                            group.extend(is_download_comment)
                    link_type = LinkType.comment if is_download_comment else LinkType.group
                    self.app.link_info[msg_link] = {'link_type': link_type,
                                                    'member_num': len(group),
                                                    'complete_num': 0,
                                                    'file_name': set()}
                    console.log(
                        f'{KeyWord.CHANNEL}:"{chat_name}",'  # 频道名。
                        f'{KeyWord.LINK}:"{msg_link}",'  # 链接。
                        f'{KeyWord.LINK_TYPE}:{LinkType.t(link_type)}。')  # 链接类型。
                    [await self.__add_task(msg_link, msg_group, retry_count) for msg_group in group]

                elif res is False and group is None:  # 单文件。
                    link_type = LinkType.single
                    self.app.link_info[msg_link] = {'link_type': link_type,
                                                    'member_num': 1,
                                                    'complete_num': 0,
                                                    'file_name': set()}
                    console.log(
                        f'{KeyWord.CHANNEL}:"{chat_name}",'  # 频道名。
                        f'{KeyWord.LINK}:"{msg_link}",'  # 链接。
                        f'{KeyWord.LINK_TYPE}:{LinkType.t(link_type)}。')  # 链接类型。
                    await self.__add_task(msg_link, msg, retry_count)
                elif res is None and group is None:
                    error = '消息不存在,频道已解散或未在频道中'
                    self.app.failure_link[msg_link] = error
                    log.warning(
                        f'{KeyWord.LINK}:"{msg_link}"{error},{Status.SKIP}。')
                elif res is None and group == 0:
                    log.error(f'读取"{msg_link}"时出现未知错误,{Status.SKIP}。')
            except UnicodeEncodeError as e:
                error = '频道标题存在特殊字符,请移步终端下载'
                self.app.failure_link[msg_link] = e
                log.error(f'{KeyWord.LINK}:"{msg_link}"{error},{KeyWord.REASON}:"{e}"')
            except MsgIdInvalid as e:
                self.app.failure_link[msg_link] = e
                log.error(f'{KeyWord.LINK}:"{msg_link}"消息不存在,可能已删除,{Status.SKIP}。{KeyWord.REASON}:"{e}"')
            except UsernameInvalid as e:
                self.app.failure_link[msg_link] = e
                log.error(
                    f'{KeyWord.LINK}:"{msg_link}"频道用户名无效,该链接的频道用户名可能已更改或频道已解散,{Status.SKIP}。{KeyWord.REASON}:"{e}"')
            except Exception as e:
                self.app.failure_link[msg_link] = e
                log.error(
                    f'{KeyWord.LINK}:"{msg_link}"未收录到的错误,{Status.SKIP}。{KeyWord.REASON}:"{e}"')
        else:
            await self.__add_task(msg_link, message, retry_count)

    def __process_links(self, link: str or list) -> set or None:
        """将链接(文本格式或链接)处理成集合。"""
        start_content: str = 'https://t.me/'
        msg_link_set: set = set()
        if isinstance(link, str):
            if link.endswith('.txt') and os.path.isfile(link):
                with open(file=link, mode='r', encoding='UTF-8') as _:
                    links: list = [content.strip() for content in _.readlines()]
                for link in links:
                    if link.startswith(start_content):
                        msg_link_set.add(link)
                    else:
                        log.warning(f'"{link}"是一个非法链接,{KeyWord.STATUS}:{Status.SKIP}。')
            elif link.startswith(start_content):
                msg_link_set.add(link)
        elif isinstance(link, list):
            for i in link:
                res = self.__process_links(link=i)
                if res is not None:
                    msg_link_set.update(res)
        if len(msg_link_set) > 0 and msg_link_set is not None:
            return msg_link_set
        elif not self.app.bot_token:
            console.log('没有找到有效链接,程序已退出。')
            sys.exit()

    async def __download_media_from_links(self) -> None:
        await self.client.start()
        self.app.progress.start()  # v1.1.8修复登录输入手机号不显示文本问题。
        if self.app.bot_token is not None:
            result = await self.start_bot(pyrogram.Client(
                name=self.app.BOT_NAME,
                api_hash=self.app.api_hash,
                api_id=self.app.api_id,
                bot_token=self.app.bot_token,
                workdir=self.app.work_directory,
                proxy=self.app.enable_proxy
            ))
            console.log(result, style='#B1DB74' if self.is_running else '#FF4689')
        links = self.__process_links(link=self.app.links)
        # 将初始任务添加到队列中。
        for link in links:
            await self.__create_download_task(msg_link=link)
        # 处理队列中的任务。
        while not self.queue.empty():
            task = await self.queue.get()
            if isinstance(task, tuple):
                msg_link, message, retry_count = task
                await self.__create_download_task(msg_link=msg_link, message=message, retry_count=retry_count)
            else:
                await task
            self.queue.task_done()
        # 等待所有任务完成。
        await self.queue.join()

    def run(self) -> None:
        record_error: bool = False
        was_client_run: bool = False

        try:
            MetaData.print_meta()
            self.app.print_config_table()
            self.client.run(self.__download_media_from_links())
            if self.app.bot_token:
                loop = asyncio.get_event_loop()
                loop.run_until_complete(self.bot_event_loop())
            was_client_run: bool = True
        except (SessionRevoked, AuthKeyUnregistered, SessionExpired, ConnectionError) as e:
            log.error(f'登录时遇到错误,{KeyWord.REASON}:"{e}"')
            res: bool = safe_delete(file_p_d=os.path.join(self.app.DIRECTORY_NAME, 'sessions'))
            record_error: bool = True
            if res:
                log.warning('已删除旧会话文件,请重启软件。')
            else:
                log.error('账号已失效,请手动删除软件目录下的sessions文件夹后重启软件。')
        except AttributeError as e:
            self.app.progress.stop()
            record_error: bool = True
            log.error(f'登录超时,请重新打开软件尝试登录,{KeyWord.REASON}:"{e}"')
        except KeyboardInterrupt:
            self.app.progress.stop()
            console.log('用户手动终止下载任务。')
        except Exception as e:
            self.app.progress.stop()
            record_error: bool = True
            log.exception(msg=f'运行出错,{KeyWord.REASON}:"{e}"', exc_info=True)
        finally:
            if self.client.is_connected:
                was_client_run: bool = True
                self.client.stop()
            self.app.progress.stop()
            if not record_error:
                self.app.print_media_table()
                self.app.print_failure_table() if self.app.failure_link else None  # v1.1.2 增加下载失败的链接统计,但如果没有失败的链接将不会显示。
                # todo 打印链接信息表格。
                MetaData.pay()
                self.app.process_shutdown(60) if was_client_run else None  # v1.2.8如果并未打开客户端执行任何下载,则不执行关机。
            os.system('pause') if self.app.platform == 'Windows' else console.input('请按「Enter」键继续. . .')

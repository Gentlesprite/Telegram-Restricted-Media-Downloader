# coding=UTF-8
# Author:Gentlesprite
# Software:PyCharm
# Time:2025/1/24 21:27
# File:bot.py
import asyncio
from typing import List, Dict

import pyrogram
from pyrogram.handlers import MessageHandler, CallbackQueryHandler
from pyrogram.types import BotCommand, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

from module import __version__, __copyright__, SOFTWARE_FULL_NAME, __license__
from module.enum_define import BotCommandText, BotMessage


class Bot:
    commands: List[BotCommand] = [BotCommand(BotCommandText.help[0], BotCommandText.help[1]),
                                  BotCommand(BotCommandText.download[0], BotCommandText.download[1].replace('`', '')),
                                  BotCommand(BotCommandText.exit[0], BotCommandText.exit[1])]

    def __init__(self):
        self.bot = None
        self.last_bot_message = None
        self.is_bot_running: bool = False
        self.bot_task_link: set = set()

    async def process_error_message(self,
                                    client: pyrogram.Client,
                                    message: pyrogram.types.Message) -> None:
        await self.help(client, message)
        self.last_bot_message = await client.send_message(chat_id=message.chat.id,
                                                          text='未知命令,请查看帮助后重试。',
                                                          disable_web_page_preview=True)

    async def get_link_from_bot(self,
                                client: pyrogram.Client,
                                message: pyrogram.types.Message) -> Dict[str, set] or None:
        text: str = message.text
        if text == '/download':

            self.last_bot_message = await client.send_message(chat_id=message.chat.id,
                                                              text='请提供下载链接,格式:\n`/download https://t.me/x/x`',
                                                              disable_web_page_preview=True)
        elif text.startswith('https://t.me/'):

            if text[len('https://t.me/'):].count('/') >= 1:
                self.last_bot_message = await client.send_message(chat_id=message.chat.id,
                                                                  text=f'请使用以下命令,分配下载任务:\n`/download {text}`',
                                                                  disable_web_page_preview=True)
            else:
                self.last_bot_message = await client.send_message(chat_id=message.chat.id,
                                                                  text=f'请使用以下命令,分配下载任务:\n`/download https://t.me/x/x`',
                                                                  disable_web_page_preview=True)
        elif len(text) <= 25 or text == '/download https://t.me/x/x' or text.endswith('.txt'):
            await self.help(client, message)
            self.last_bot_message = await client.send_message(chat_id=message.chat.id,
                                                              text='链接错误,请查看帮助后重试。',
                                                              disable_web_page_preview=True)
        else:
            n = '\n'
            link: list = text.split()
            link.remove('/download') if '/download' in link else None
            right_link: set = set([_ for _ in link if _.startswith('https://t.me/')])
            exist_link: set = set([_ for _ in link if _ in self.bot_task_link])
            right_link -= exist_link
            invalid_link: set = set([_ for _ in link if not _.startswith('https://t.me/')])
            self.bot_task_link.update(right_link)
            right_msg: str = f'{BotMessage.right}`{n.join(right_link)}`' if right_link else ''
            exist_msg: str = f'{BotMessage.exist}`{n.join(exist_link)}`' if exist_link else ''
            invalid_msg: str = f'{BotMessage.invalid}`{n.join(invalid_link)}`' if invalid_link else ''
            self.last_bot_message = await client.send_message(chat_id=message.chat.id,
                                                              text=right_msg + n + exist_msg + n + invalid_msg,
                                                              disable_web_page_preview=True)
            if len(right_link) >= 1:
                return {'right_link': right_link, 'exist_link': exist_link, 'error_link': invalid_link}
            else:
                return None

    async def help(self,
                   client: pyrogram.Client,
                   message: pyrogram.types.Message) -> None:
        update_keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        '📦GitHub',
                        url='https://github.com/Gentlesprite/Telegram_Restricted_Media_Downloader/releases',
                    ),
                    InlineKeyboardButton(
                        '📌订阅频道', url='https://t.me/RestrictedMediaDownloader'
                    )
                ],
                [
                    InlineKeyboardButton(
                        '🎬视频教程',
                        url='https://www.bilibili.com/video/BV1nCp8evEwv'),
                    InlineKeyboardButton(
                        '💰支持作者',
                        callback_data='pay')
                ]
            ]
        )

        msg = (
            f'`\n💎 {SOFTWARE_FULL_NAME} v{__version__} 💎\n'
            f'©️ {__copyright__.replace(" <https://github.com/Gentlesprite>", ".")}\n'
            f'📖 Licensed under the terms of the {__license__}.`\n'
            f'🎮️ 可用命令:\n'
            f'🛎 {BotCommandText.with_description(BotCommandText.help)}\n'
            f'📁 {BotCommandText.with_description(BotCommandText.download)}\n'
            f'❌ {BotCommandText.with_description(BotCommandText.exit)}\n\n'
        )

        self.last_bot_message = await client.send_message(chat_id=message.chat.id,
                                                          text=msg,
                                                          disable_web_page_preview=True,
                                                          reply_markup=update_keyboard)

    @staticmethod
    async def pay_callback(client: pyrogram.Client, callback_query: CallbackQuery) -> None:
        await callback_query.answer()
        await callback_query.message.reply_text(
            '🙏🥰🙏收款「二维码」已发送至您的「终端」与「对话框」十分感谢您的支持!')

    async def exit(self, client: pyrogram.Client,
                   message: pyrogram.types.Message) -> None:
        self.is_bot_running = False

    async def start_bot(
            self,
            bot_client_obj: pyrogram.Client,
    ) -> str:
        """启动机器人。"""
        try:
            self.bot = bot_client_obj
            await bot_client_obj.start()
            await self.bot.set_bot_commands(self.commands)
            self.bot.add_handler(
                MessageHandler(
                    self.help,
                    filters=pyrogram.filters.command(['help', 'start'])
                )
            )
            self.bot.add_handler(
                MessageHandler(
                    self.get_link_from_bot,
                    filters=pyrogram.filters.command(['download'])
                )
            )

            self.bot.add_handler(
                MessageHandler(
                    self.exit,
                    filters=pyrogram.filters.command(['exit'])
                )
            )

            self.bot.add_handler(MessageHandler(
                self.get_link_from_bot,
                filters=pyrogram.filters.regex(r'^https://t.me.*'))
            )
            self.bot.add_handler(
                CallbackQueryHandler(
                    self.pay_callback,
                    filters=pyrogram.filters.regex('pay')
                )
            )
            self.bot.add_handler(MessageHandler(
                self.process_error_message
            ))
            self.is_bot_running: bool = True
            return '「机器人」启动成功。'
        except Exception as e:
            self.is_bot_running: bool = False
            return f'「机器人」启动失败,原因:"{e}"'

    async def bot_event_loop(self):
        while self.is_bot_running:
            await asyncio.sleep(0.5)  # 解决资源占用过多问题。

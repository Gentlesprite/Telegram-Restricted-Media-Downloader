# coding=UTF-8
# Author:Gentlesprite
# Software:PyCharm
# Time:2025/1/24 21:27
# File:bot.py
import asyncio
from typing import List
import pyrogram
from pyrogram.handlers import MessageHandler, CallbackQueryHandler

from pyrogram.types import BotCommand, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from module import __version__, SOFTWARE_FULL_NAME, AUTHOR
from module.enum_define import BotCommentText


class Bot:
    commands: List[BotCommand] = [BotCommand(BotCommentText.help[0], BotCommentText.help[1]),
                                  BotCommand(BotCommentText.download[0], BotCommentText.download[1].replace('`', '')),
                                  BotCommand(BotCommentText.exit[0], BotCommentText.exit[1])]

    def __init__(self):
        self.client = None
        self.bot = None
        self.message = None
        self.is_running: bool = True

    async def process_error_message(self,
                                    client: pyrogram.Client,
                                    message: pyrogram.types.Message):
        await self.help(client,
                        message)
        await client.send_message(message.chat.id, '未知命令,请查看帮助后重试。')

    async def get_link_from_bot(self,
                                client: pyrogram.Client,
                                message: pyrogram.types.Message):
        text: str = message.text
        if text == '/download':
            self.message = None
            await client.send_message(message.chat.id, '请提供下载链接,格式:\n`/download https://t.me/x/x`')
        elif text.startswith('https://t.me/'):
            self.message = None
            if text[len('https://t.me/'):].count('/') >= 1:
                await client.send_message(message.chat.id, f'请使用以下命令,分配下载任务:\n`/download {text}`')
            else:
                await client.send_message(message.chat.id,
                                          f'请使用以下命令,分配下载任务:\n`/download https://t.me/x/x`')
        elif len(text) <= 25 or text == '/download https://t.me/x/x':
            self.message = None
            await self.help(client, message)
            await client.send_message(message.chat.id, '链接错误,请查看帮助后重试。')
        else:
            link: list = text.split()
            link.remove('/download') if '/download' in link else None
            error_link: list = [i for i in link if not i.startswith('https://t.me/')]
            right_link: list = [i for i in link if i.startswith('https://t.me/')]
            error_msg: str = f'\n以下链接不合法:\n`{" ".join(error_link)}`\n已被移除。' if error_link else ''
            add_msg: str = f'已将`{" ".join(right_link)}`分配至下载任务。' if right_link else ''
            await client.send_message(message.chat.id, add_msg + error_msg)
            if len(right_link) >= 1:
                self.message = right_link
            else:
                self.message = None

    @staticmethod
    async def help(client: pyrogram.Client,
                   message: pyrogram.types.Message):
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
            f'`\n💎 {SOFTWARE_FULL_NAME}\n'
            f'🚀 版本:{__version__}\n'
            f'👨‍💻 作者:@{AUTHOR}`\n'
            f'🕹 可用命令:\n'
            f'🛎 {BotCommentText.with_description(BotCommentText.help)}\n'
            f'📁 {BotCommentText.with_description(BotCommentText.download)}\n'
            f'❌ {BotCommentText.with_description(BotCommentText.exit)}\n\n'
        )

        await client.send_message(message.chat.id, msg, reply_markup=update_keyboard)

    @staticmethod
    async def pay_callback(client: pyrogram.Client, callback_query: CallbackQuery):
        await callback_query.answer()
        await callback_query.message.reply_text(
            '🙏😀🙏收款「二维码」已发送至您的「终端」,感谢您的支持!🙏🥰🙏')

    async def exit(self, client: pyrogram.Client,
                   message: pyrogram.types.Message):
        self.message = '/exit'

    async def start_bot(
            self,
            bot_client_obj: pyrogram.Client,
    ):
        """Start bot"""
        self.bot = bot_client_obj
        await bot_client_obj.start()
        await self.bot.set_bot_commands(self.commands)
        self.bot.add_handler(
            MessageHandler(
                self.help,
                filters=pyrogram.filters.command(['help'])
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

    async def task_chat(self):
        while self.is_running:
            if self.message == '/exit':
                self.is_running = False
                await self.bot.stop()
            else:
                await asyncio.sleep(0)

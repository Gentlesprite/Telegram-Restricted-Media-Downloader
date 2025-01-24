# coding=UTF-8
# Author:Gentlesprite
# Software:PyCharm
# Time:2025/1/24 21:27
# File:bot.py
import asyncio
import pyrogram
from pyrogram.handlers import MessageHandler
from module import console


class Bot:
    def __init__(self):
        self.client = None
        self.bot = None
        self.message = None
        self.is_running: bool = True

    async def get_link_from_bot(self,
                                client: pyrogram.Client,
                                message: pyrogram.types.Message):
        text: str = message.text
        console.print(text)
        await client.send_message(message.chat.id, f'我已收到"{text}"。')
        self.message = text

    async def start_bot(
            self,
            bot_client_obj,
    ):
        """Start bot"""
        self.bot = bot_client_obj
        await bot_client_obj.start()

    async def stop(self):
        await self.bot.stop()

    async def add_handler(self):
        self.bot.add_handler(MessageHandler(
            self.get_link_from_bot,
            filters=pyrogram.filters.regex(r"^https://t.me.*"))
        )

    async def task_chat(self):
        while self.is_running:
            if self.message == '/stop':
                self.is_running = False
            await asyncio.sleep(0)

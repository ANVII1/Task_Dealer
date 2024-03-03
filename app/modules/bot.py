from aiogram import Bot
from aiogram import Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.types import Message 
from aiohttp import web
import os
import asyncio
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiogram.types import BotCommand
import logging as l
from utils.envvars import BASE_WEBHOOK_URL, WEBHOOK_PATH, WEBHOOK_SSL_CERT,WEBHOOK_MODE, WEB_SERVER_PORT, BOT_TOKEN

log_dir = "Bot ::: "

class dealer_bot:
    bot: Bot
    dp : Dispatcher

    @classmethod
    async def send_message(self, user_id:int, message:str, reply_markup = None):
        """
        Отправка сообщения    
        """

        await self.bot.send_message(user_id,text=message,reply_markup=reply_markup)

    @classmethod
    def run(self):
        """
        Инициализирует и запускает бота
        """

        from handlers import dp
        self.dp = dp
        self.bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)

        #region setting dispatcher startup and shutdown func's
        async def on_startup(bot: Bot) -> None:
            await self._setup_bot_commands()
            if WEBHOOK_MODE:
                await self.bot.set_webhook(f"{BASE_WEBHOOK_URL}{WEBHOOK_PATH}")                

        async def on_shutdown(bot: Bot) -> None:
            l.info(log_dir + "shutted down")
            await bot.delete_webhook(drop_pending_updates=True)

        self.dp.startup.register(on_startup)
        self.dp.shutdown.register(on_shutdown)
        

        if WEBHOOK_MODE:

            # If you have a self-signed SSL certificate, then you will need to send a public
            # certificate to Telegram            
            self.start_with_webhook()            
        else:
            asyncio.run(self.polling())
             


    @classmethod
    async def _setup_bot_commands(self):
        """
        Set basic bot commands in bot menu
        """
        commands = [
            ["start","страт"],
            ["echo","эхо"]
        ]

        # // transform simple array to BotCommand object array
        commandList =[]
        for command in commands:
            commandList.append(BotCommand(command=command[0], description=command[1]))

        await self.bot.set_my_commands(commands=commandList)


    @classmethod
    async def polling(self):
        """
        start's app with longpolling
        """

        l.info(log_dir + "start with polling")
        await self.dp.start_polling(self.bot, allowed_updates=self.dp.resolve_used_update_types())


    @classmethod
    def start_with_webhook(self):
        """
        starts app with webhook
        """
        app = web.Application()

        webhook_requests_handler = SimpleRequestHandler(
            dispatcher=self.dp,
            handle_in_background=True,
            bot=self.bot)

        webhook_requests_handler.register(app, path=WEBHOOK_PATH)

        setup_application(app, self.dp, bot=self.bot)

        # And finally start webserver
        l.info(log_dir + "started with webhook")
        web.run_app(app, host="0.0.0.0", port=int(WEB_SERVER_PORT))
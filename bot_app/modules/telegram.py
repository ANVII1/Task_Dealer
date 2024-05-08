from aiogram import Bot
from aiogram import Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.types import Message 
from aiohttp import web
import asyncio
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiogram.types import BotCommand
from modules.logging import logger as l
from utils import envvars
from abc import ABC

_log_dir = "Bot " 
class bots:
    botlist:dict = {}
    
    @classmethod
    def get_by_name(self,bot_name:str) -> Bot|None :
        if not (bot_name in self.botlist.keys()):
            return None
        
        return self.botlist[bot_name]

    @classmethod
    async def create_bot(self,bot_name:str,token:str,dp:Dispatcher,commands:list[list[str]]) -> Bot: 
        bot = Bot(token=token, parse_mode=ParseMode.MARKDOWN_V2)
        
        self.botlist[bot_name] = bot
        # setup bot commands in telegram
        preprocessed_commands =[]
        for command in commands:
            preprocessed_commands.append(BotCommand(command=command[0], description=command[1]))

        await bot.set_my_commands(commands=preprocessed_commands)
        # setup startup/shutdown funcs
        async def __on_startup(bot: Bot) -> None:            
            pass                            

        async def __on_shutdown(bot: Bot) -> None:
            l.inf(_log_dir + "shutted down")
            await bot.delete_webhook(drop_pending_updates=True)

        dp.startup.register(__on_startup)
        dp.shutdown.register(__on_shutdown)

        if not envvars.WEBHOOK_MODE:
            await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
            l.inf(_log_dir + "start with polling")
        else:        
            app = web.Application()

            webhook_requests_handler = SimpleRequestHandler(
                dispatcher=dp,
                handle_in_background=True,
                bot=bot)

            webhook_requests_handler.register(app, path=envvars.WEBHOOK_PATH)

            setup_application(app, dp, bot=bot)
            
            # If you have a self-signed SSL certificate, then you will need to send a public
            # certificate to Telegram
            await bot.set_webhook(f"{envvars.BASE_WEBHOOK_URL}{envvars.WEBHOOK_PATH}")

            # And finally start webserver
            web.run_app(app, host="0.0.0.0", port=int(envvars.WEB_SERVER_PORT),loop=asyncio.get_event_loop())        
            l.inf(_log_dir + "started with webhook")
        

#region current_bots
async def built_dealer() -> None:
    from handlers import dp
    token = envvars.BOT_TOKEN
    commands = [
        ["start","старт"],
        ["ohfuck","бля"],
        ["echo","эхо"]
    ]
    
    await bots.create_bot("DEALER",token,dp,commands) 
    
#endregion

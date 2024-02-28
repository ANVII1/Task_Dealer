from dotenv  import load_dotenv
load_dotenv() # loading envirement variables before load's bot module bc's it needs token in env

from modules.bot import bot,Bot
import asyncio
import ssl
from handlers import dp
import logging as l
from aiohttp import web
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
import os
from aiogram.types import FSInputFile
from aiogram.types import BotCommand

# WEB_SERVER_HOST = os.environ['WEB_SERVER_HOST']
# WEB_SERVER_PORT = os.environ['WEB_SERVER_PORT']
# WEBHOOK_SSL_CERT = "/app/iskr.pem"
# WEBHOOK_SSL_PRIV = "/app/iskr.key"
# WEBHOOK_PATH = "/bot"
# BASE_WEBHOOK_URL = f"{WEB_SERVER_HOST}:{WEB_SERVER_PORT}"

def setup_logging():
    """
    Setup logging settings
    """
    l.basicConfig(
    level=l.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    filename="logs.log"
    )

async def setup_bot_commands():
    """
    Set basic bot command in bot menu
    """
    commands = [
        ["status","Текущий статус"],
        ["trainingmenu","Меню тренеровок"],
        ["qr","Генерация QR-кода"],
        ["sendsticker","Пришли стикер"],
        ["mode","Режим работы Искры"]
    ]
    commandList =[]
    for command in commands:
        commandList.append(BotCommand(command=command[0], description=command[1]))
    await bot.set_my_commands(commands=commandList)

async def on_startup(bot: Bot) -> None:
    if os.environ['WEBHOOK'] == "1":
        await bot.set_webhook(f"{BASE_WEBHOOK_URL}{WEBHOOK_PATH}",
            certificate=FSInputFile(WEBHOOK_SSL_CERT),
                )
    await setup_bot_commands()

async def on_shutdown(bot: Bot) -> None:
    l.info("bot shutted down")
    await bot.delete_webhook(drop_pending_updates=True)

async def polling():
    l.info("start with polling")
    setup_logging()
    Scheduler.init(asyncio.get_event_loop())
    await TW.StartTask()
    await setup_bot_commands()
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

def start_with_webhook():
    
    
    app = web.Application()

    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        handle_in_background=True,
        bot=bot
    )

    webhook_requests_handler.register(app, path=WEBHOOK_PATH)

    setup_application(app, dp, bot=bot)

    # And finally start webserver
    l.info("started with webhook")
    web.run_app(app, host="0.0.0.0", port=int(WEB_SERVER_PORT))


def main() -> None:
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    setup_logging()
    if os.environ['WEBHOOK'] == "0":
        asyncio.run(polling())
    else:
        start_with_webhook()        
    l.info("Start Working")
    
if __name__ == "__main__":
    main()
from dotenv  import load_dotenv
load_dotenv()
from modules.bot import bot,Bot
import asyncio
import ssl
from handlers import dp
from modules.anvSched import Scheduler
from wrappers.TrainingWrapper import TrainingWrapper as TW
import logging
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
        logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        filename="logs.log"
        )

async def setup_bot_commands():
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
    Scheduler.init(asyncio.get_event_loop())
    await TW.StartTask()
    await setup_bot_commands()

async def on_shutdown(bot: Bot) -> None:
    logging.info("bot shutted down")
    await bot.delete_webhook(drop_pending_updates=True)

async def polling():
    logging.info("start with polling")
    setup_logging()
    Scheduler.init(asyncio.get_event_loop())
    await TW.StartTask()
    await setup_bot_commands()
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

def main() -> None:
    

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    app = web.Application()

    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        handle_in_background=True,
        bot=bot
    )

    webhook_requests_handler.register(app, path=WEBHOOK_PATH)

    setup_application(app, dp, bot=bot)

    # Generate SSL context
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(WEBHOOK_SSL_CERT, WEBHOOK_SSL_PRIV)
    
    # And finally start webserver
    logging.info("started with webhook")
    web.run_app(app, host="0.0.0.0", port=int(WEB_SERVER_PORT), ssl_context=context)

    
if __name__ == "__main__":
    setup_logging()
    if os.environ['WEBHOOK'] == "0":
        asyncio.run(polling())
    else:
        main()
    logging.info("Start Working")
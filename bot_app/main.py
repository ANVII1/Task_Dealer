from utils.envvars import WEBHOOK_MODE, BOT_TOKEN
from modules.telegram import bots, built_dealer
import modules.scheduler.anvSched as Scheduler
import asyncio  

from modules.logging import logger as l


async def main() -> None:

    l.wrn("Main Starting Working")    

    await Scheduler.init()    
    await built_dealer()    
    
if __name__ == "__main__":
    asyncio.run(main())
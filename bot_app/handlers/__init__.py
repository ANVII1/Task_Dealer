from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import BaseMiddleware
from typing import Dict,Any,Awaitable,Callable
from aiogram.types import Message
from utils import envvars
from modules.logging import logger as l

from handlers import (commands as commands,
                      common as common,
                      newUser as newUser,
                      newTask as newTask
                      )

dp = Dispatcher(storage=MemoryStorage())

class firewall(BaseMiddleware):
    async def __call__(        
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
            ) -> Any:
        if str(event.from_user.id) != envvars.MASTER:
            l.wrn(f"Firewall Blocked Enemy ::: Enemy id - {event.from_user.id}")
            return
        return await handler(event, data)
        

dp.message.middleware.register(firewall())

dp.include_routers(
    commands.router,
    newTask.router,
    newUser.router,
    common.router,
    )
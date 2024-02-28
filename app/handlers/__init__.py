from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from handlers import (commands as commands,
                      common as common
                      )

dp = Dispatcher(storage=MemoryStorage())

dp.include_routers(
    commands.router,
    common.router
    )
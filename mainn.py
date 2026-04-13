#aio
import asyncio
from aiogram import Bot,Dispatcher


#env
from dotenv import load_dotenv

#routers
from handlers import start_router
from handlers import help_router
from handlers import gpt_router
from handlers import capy_router
from handlers import info_router    
from handlers import mango_router
from handlers import tap_router
from handlers import dudos_router
from handlers import idea_router


#lib
import os
from controller import get_current_time
from logging_bot import log_to_file,try_ex_deco

#config
load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
dp = Dispatcher()


#handlers
dp.include_router(start_router)
dp.include_router(help_router)
dp.include_router(gpt_router)
dp.include_router(capy_router)
dp.include_router(info_router)
dp.include_router(mango_router)
dp.include_router(tap_router)
dp.include_router(dudos_router)
dp.include_router(idea_router)

async def start():
    bot = Bot(token=BOT_TOKEN)
    log_to_file('БОТ ЗАПУЩЕН')

    print('starting...')
    await dp.start_polling(bot)

asyncio.run(start())





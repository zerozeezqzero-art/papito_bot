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



#lib
import os
from datetime import datetime
from controller import get_current_time

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



async def start():
    bot = Bot(token=BOT_TOKEN)
    with open('bot_log.txt', 'a',encoding='UTF-8') as f:
        f.write(f"{get_current_time()} - Бот запущен!\n")

    print('starting...')
    await dp.start_polling(bot)

asyncio.run(start())


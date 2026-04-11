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
    
    print('starting...')
    await dp.start_polling(bot)

asyncio.run(start())


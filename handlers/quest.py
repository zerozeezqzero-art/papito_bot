#aio
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
#modules import
from logging_bot import try_ex_deco
from logging_bot import log_to_file
from controller import Capybara_Controller

router = Router()

@router.message(Command('quest'))
@try_ex_deco
async def quest_command(message):
    capy = Capybara_Controller(message)
    result, success = capy.get_quest(message)
    await message.answer(result, parse_mode="Markdown")
    capy.close()
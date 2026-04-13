#aio
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import FSInputFile,InlineKeyboardButton,InlineKeyboardMarkup

#modules import
from controller import Capybara_Controller
from .help import help_command
from logging_bot import log_to_file
from logging_bot import try_ex_deco
import random


router = Router()

@router.message(Command('start'))
@try_ex_deco
async def start_command(message):
    capy = Capybara_Controller(message)
    log_to_file(f"➡️ Пользователь {capy.usern} написал команду /start")

    if capy.is_troll_mode(message.from_user.username):
        if random.randint(0, 1) == 0:
            await message.answer('ОШИБКА!❌')
            capy.close()
            return
        else:
            pass
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="➡️  ЧТО Я УМЕЮ  ⬅️", callback_data="help")]
    ])


    copibara = FSInputFile(capy.images['greeting_photo'])
    await message.answer_photo(copibara,caption="",reply_markup=keyboard)
    capy.close()



@router.callback_query(lambda c: c.data == "help")
async def help_callback(callback_query):
    await callback_query.answer()
    
    await help_command(callback_query.message)
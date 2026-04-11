#aio
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import FSInputFile,InlineKeyboardButton,InlineKeyboardMarkup,SwitchInlineQueryChosenChat

#modules import
from controller import Capybara_Controller
from .help import help_command

#lib
import random



router = Router()

@router.message(Command('start'))
async def start_command(message):

    capy = Capybara_Controller(message)
    print(f"➡️ Пользователь {capy.usern} написал команду /start")

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
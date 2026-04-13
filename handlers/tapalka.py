
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import FSInputFile,InlineKeyboardButton,InlineKeyboardMarkup,Message,callback_query


#modules import
from controller import Capybara_Controller
from logging_bot import log_to_file
from logging_bot import try_ex_deco
from logging_bot import troll_check


router = Router()

@router.message(Command('tapalka'))
@troll_check
@try_ex_deco
async def tapalka_command(message):
    capy = Capybara_Controller(message)
    log_to_file(f'пользователь {capy.usern} написал команду /tapalka')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='👆 Тап сюда — +1 папито токен', callback_data='tap')]
])
    await message.answer("Нажми на кнопку, чтобы получить монету!",reply_markup=keyboard)

@router.callback_query(lambda c: c.data == 'tap')
@try_ex_deco
async def tap_callback(callback):
    class FakeMessage:
        from_user = callback.from_user
    
    capy = Capybara_Controller(FakeMessage())
    result, success = capy.tapalka(FakeMessage())
    
    await callback.message.answer(result)
    await callback.answer()
    capy.close()
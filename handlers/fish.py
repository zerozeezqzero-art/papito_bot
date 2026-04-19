from aiogram import Router
from aiogram.types import Message,FSInputFile,InlineKeyboardButton,InlineKeyboardMarkup,CallbackQuery
from aiogram.filters import Command

from controller import Capybara_Controller
from logging_bot import log_to_file,try_ex_deco


router = Router()


@router.message(Command('fish'))
@try_ex_deco
async def fish_command(message:Message):
    capy = Capybara_Controller(message)
    log_to_file(f'Пользователь {capy.usern} Написал команду /fish')
    button = InlineKeyboardButton(
        text="🐟 ПОЙМАТЬ РЫБУ 🎣",
        callback_data="ribalka"
    )
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button]])
    await message.answer("🎣Для рыбалки нажми на кнопку снизу", reply_markup=keyboard)
    capy.close()



@router.callback_query(lambda c: c.data == 'ribalka')
@try_ex_deco
async def ribalka(callback: CallbackQuery):
    class FakeMessage:
        from_user = callback.from_user
    
    fk = FakeMessage()
    capy = Capybara_Controller(fk)
    
    result, success, quest_completed, quest_reward = capy.fishing(fk)
    
    if quest_completed:
        await callback.message.answer(f"🎉 Квест выполнен! +{quest_reward} токенов!")
    
    if success:
        await callback.message.answer_photo(FSInputFile(capy.images['capy_fish']), caption=result)
    else:
        await callback.message.answer(result)
    
    await callback.answer()
    capy.close()

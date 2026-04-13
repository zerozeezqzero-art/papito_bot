from aiogram import Router
from aiogram.types import Message,FSInputFile
from aiogram.filters import Command

from controller import Capybara_Controller
from logging_bot import log_to_file,try_ex_deco
router = Router()

@router.message(Command('buy_mango'))
@try_ex_deco
async def buy_mango_command(message: Message):
    capy = Capybara_Controller(message)
    log_to_file(f'Пользователь {capy.usern} написал команду /buy_mango')
    result,successful = capy.buy_mangomon(message)
    if successful:
        photo = capy.images['mangomons'][result]
        texts = {
        'basic_mango': '🎉 Базовый мангомон! (60%),Он снижает кд кормления на 2 минуты',
        'epic_mango': '🎉 Эпический мангомон! (25%),Он снижает кд кормления на 2 минуты + 500 токенов',
        'mythic_mango': '🔥 МИФИЧЕСКИЙ мангомон! (10%),Он снижает кд кормления на 2 минуты + 500 токенов + Повышение шанса на выйгрыш в лотерее',
        'legendary_mango': '👑 ЛЕГЕНДАРНЫЙ мангомон! (5%),Он снижает кд кормления на 3 минуты + за повышение уровня дается не 25 а 125 папито токенов'}
        await message.answer_photo(FSInputFile(photo), caption=texts.get(result))
    else:
        await message.answer(result)
    capy.close()
    



@router.message(Command('my_mango'))
@try_ex_deco
async def my_mango_command(message: Message):
    capy = Capybara_Controller(message)
    log_to_file(f'Пользователь {capy.usern} написал команду /my_mango')
    result,successful = capy.get_my_mango(message)
    texts = {
        'basic_mango': '🎉 Базовый мангомон! (60%),Он снижает кд кормления на 2 минуты',
        'epic_mango': '🎉 Эпический мангомон! (25%),Он снижает кд кормления на 2 минуты + 500 токенов',
        'mythic_mango': '🔥 МИФИЧЕСКИЙ мангомон! (10%),Он снижает кд кормления на 2 минуты + 500 токенов + Повышение шанса на выйгрыш в лотерее',
        'legendary_mango': '👑 ЛЕГЕНДАРНЫЙ мангомон! (5%),Он снижает кд кормления на 3 минуты + за повышение уровня дается не 25 а 125 папито токенов'}
    
    if successful:
        photo = capy.images['mangomons'].get(result)
        await message.answer_photo(FSInputFile(photo), caption=texts.get(result, result))
    else:
        await message.answer(result)




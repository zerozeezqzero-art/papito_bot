#aio
from aiogram import Router
from aiogram.filters import Command
#modules import
from logging_bot import try_ex_deco
from logging_bot import log_to_file
from controller import Capybara_Controller

router = Router()

@router.message(Command('info'))
@try_ex_deco
async def info_command(message):
        capy = Capybara_Controller(message)
        log_to_file(f'пользователь {capy.usern} написал команду /info')
        await message.answer("этого бота создали два талантливых одаренных мальчика ХАКЕРЫ @deadNANASHI и @ruby_skull, после распада попитоляндии это был их последний вкалд в империю В СОЗДАНИИ ЭТОГО БОТА БЫЛИ ВОВЛЕЧЕНЫ ТОЛЬКО ОНИ, НИКТО ИЗ ДРУГИХ УЧАСТНИКОВ ПОПИТОЛЯНДИИ НЕ ДЕЛАЛ ЭТОГО БОТА КРОМЕ НИХ")


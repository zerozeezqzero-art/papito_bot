#aio
from aiogram import Router
from aiogram.filters import Command

router = Router()

@router.message(Command('info'))
async def info_command(message):
        await message.answer("этого бота создали два талантливых одаренных мальчика ХАКЕРЫ @deadNANASHI и @ruby_skull, после распада попитоляндии это был их последний вкалд в империю В СОЗДАНИИ ЭТОГО БОТА БЫЛИ ВОВЛЕЧЕНЫ ТОЛЬКО ОНИ, НИКТО ИЗ ДРУГИХ УЧАСТНИКОВ ПОПИТОЛЯНДИИ НЕ ДЕЛАЛ ЭТОГО БОТА КРОМЕ НИХ")


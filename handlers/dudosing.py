#aio
from aiogram import Router
from aiogram.filters import Command


#modules import
from controller import Capybara_Controller
from logging_bot import log_to_file
from logging_bot import try_ex_deco



router = Router()

@router.message(Command('dudosing'))
@try_ex_deco
async def dudos_command(message):
    capy = Capybara_Controller(message)
    log_to_file(f'Пользователь {capy.usern} написал команду /dudosing')
    if message.from_user.id != capy.admin_id:
         await message.answer("❌ У тебя нет прав на эту команду!")
         capy.close()
    else:
        args = message.text.split()
        if len(args) < 2:
            await message.answer("❌ Укажи username жертвы!\nПример: /dudosing ruby_skull")
            capy.close()
            return
        
        target = args[1].replace('@', '')
        
        result, success = capy.dudosing(message, target)
        await message.answer(result)
        capy.close()



@router.message(Command('stop_dudosing'))
@try_ex_deco
async def stop_dudos_command(message):
    capy = Capybara_Controller(message)
    log_to_file(f'Пользователь {capy.usern} написал команду /stop_dudosing')
    
    if message.from_user.id != capy.admin_id:
        await message.answer("❌ У тебя нет прав на эту команду!")
        capy.close()
        return
    else:
        args = message.text.split()
        if len(args) < 2:
            await message.answer("❌ Укажи username!\nПример: /stop_dudosing ruby_skull")
            capy.close()
            return
        
        target = args[1].replace('@', '')
        
        result, success = capy.stop_dudosing(message, target)
        await message.answer(result)
        capy.close()
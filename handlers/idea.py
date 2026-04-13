#aio
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
#modules import
from logging_bot import try_ex_deco
from logging_bot import log_to_file
from controller import Capybara_Controller

router = Router()

@router.message(Command('idea'))
@try_ex_deco
async def idea_command(message: Message):
        capy = Capybara_Controller(message)
        log_to_file(f'Пользователь {capy.usern} написал команду /idea')
        user_idea = message.text.replace('/idea','')
        log_to_file(f'Пользователь {capy.usern} предложил идею для бота: {user_idea}')
        with open('users_idea.txt', 'a',encoding='UTF-8') as f:
            f.write(f'{capy.usern} предложил идею {user_idea}\n')

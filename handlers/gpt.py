#aio
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import FSInputFile


#modules import
from controller import Capybara_Controller
from gpt_func import gpt_answer
from  logging_bot import log_to_file
from logging_bot import try_ex_deco
from logging_bot import troll_check
router = Router()


@router.message(Command('gpt'))
@troll_check
@try_ex_deco
async def gpt_command(message):
    capy = Capybara_Controller(message)
    log_to_file(f"➡️ Пользователь {capy.usern}  написал команду /gpt")
    user_text = message.text.replace("/gpt", "").strip()
    

    log_to_file(f"📝 Текст вопроса: {user_text}")


    if not user_text:
        log_to_file("❌ Вопрос пустой!")
        await message.answer("""❌ Ошибка: не указан вопрос
Пример правильного использования:
/gpt Расскажи про капибару""")
        return
    answer = gpt_answer(user_text)
    log_to_file("✅ Ответ получен, отправляю...")
    await message.answer_photo(FSInputFile(capy.images['gpt_photo']))
    await message.reply(answer)

#aio
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import FSInputFile


#modules import
from controller import Capybara_Controller
from gpt_func import gpt_answer

router = Router()


@router.message(Command('gpt'))
async def gpt_command(message):
    capy = Capybara_Controller(message)
    print(f"➡️ Пользователь {capy.usern}  написал команду /gpt")  # ← Увидите в консоли
    user_text = message.text.replace("/gpt", "").strip()
    

    print(f"📝 Текст вопроса: {user_text}")


    if not user_text:
        print("❌ Вопрос пустой!")
        await message.answer("""❌ Ошибка: не указан вопрос
Пример правильного использования:
/gpt Расскажи про капибару""")
        return
    try:
        answer = gpt_answer(user_text)
        print("✅ Ответ получен, отправляю...")
        await message.answer_photo(FSInputFile(capy.images['gpt_photo']))
        await message.reply(answer)
    except Exception as e:
         print(f"🔥 ОШИБКА: {e}")
         await message.answer('Ошибка, попробуйте позже')
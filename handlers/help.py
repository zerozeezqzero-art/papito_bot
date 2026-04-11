#aio
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import FSInputFile,InlineKeyboardButton,InlineKeyboardMarkup,SwitchInlineQueryChosenChat

#modules
from controller import Capybara_Controller

router = Router()

@router.message(Command('help'))
async def help_command(message):
    
    
    capy = Capybara_Controller(message)
    


    button = InlineKeyboardButton(
        text="➕ Добавить в группу",
        url=f"https://t.me/{'python_174bot'}?startgroup=start"
    )

    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button]])
    
    print(f"➡️ Пользователь {capy.usern} написал команду /help")

   
    await message.answer_photo(FSInputFile(capy.images['help_photo']),caption='''🐹 CapybaraBot — твой пушистый друг\n
🤖 /gpt "вопрос" — спросить о чём угодно у CapybaraGPT
🐾 /capybara — завести свою капибару
🍉 /capyfeed — покормить капибару (она любит вкусняшки)
📈 /capylevel — проверить уровень и прогресс
🏆 /leaderboard — топ самых прокачанных капибар
📸 /photo — случайная милая капибара
👨‍💻 /info - информация о создателях
💵 /papito_tokens - узнать баланс папито токенов
🛒 /shop - магазин за папито токены''',reply_markup=keyboard)
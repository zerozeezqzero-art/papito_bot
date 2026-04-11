#aio
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import FSInputFile,InlineKeyboardButton,InlineKeyboardMarkup,Message,callback_query


#modules import
from controller import Capybara_Controller

#lib
import random


router = Router()








@router.message(Command('capybara'))
async def capybara_command_create(message:Message):
    capy = Capybara_Controller(message)
    
    print(f"➡️ Пользователь {capy.usern} написал команду /capybara")
    
    if capy.create_capy():
        await message.answer_photo(FSInputFile(capy.images['capy_born']),caption=f'КАПИБАРА {capy.usern} СОЗДАНА!')
        capy.close()
    else:
        await message.answer('У ВАС УЖЕ ЕСТЬ КАПИБАРА!')
        capy.close()


@router.message(Command('capyfeed'))
async def capybara_command_feed(message:Message):
    capy = Capybara_Controller(message)
   
    print(f"➡️ Пользователь {capy.usern} написал команду /capyfeed")
    result, success = capy.feed_capy(message)
    
    
    if result is None:
        await message.answer('❌ У тебя нет капибары! Создай командой /capybara')
        capy.close()
        return
    
    if success:
        await message.answer(result)
    else:
        await message.answer_photo(FSInputFile(capy.images['capy_eat']), caption=result)
    
    capy.close()



@router.message(Command('capylevel'))
async def capybara_command_level(message:Message):
    capy = Capybara_Controller(message)
    print(f"➡️ Пользователь {capy.usern} написал команду /capylevel")
    lvl, success = capy.get_capy_level(message)
    if success == 'No_capy' or not success:
        await message.answer('❌ У тебя нет капибары! Создай командой /capybara')
    else:
        await message.answer(f'Уровень вашей капибары - {lvl}')
    capy.close()



@router.message(Command('leaderboard'))
async def leaderboard_command(message:Message):
    capy = Capybara_Controller(message)
    print(f"➡️ Пользователь {capy.usern} написал команду /leaderboard")
    result = capy.leaderboard()
    await message.answer_photo(FSInputFile(capy.images['capy_leader_board']),caption=result)
    capy.close()


@router.message(Command('photo'))
async def capybara_photo_command(message:Message):
    capy = Capybara_Controller(message)
    print(f"➡️ Пользователь {capy.usern} написал команду /photo")
    try:
        copibara = FSInputFile(random.choice(capy.images['random_capy']))
        await message.answer_photo(copibara, caption="вот и твоя капибара...")
    except Exception as e:
        await message.answer(f'Ошибка, попробуй позже!')
        print(e)
    finally:
        capy.close()



@router.message(Command('papito_tokens'))
async def papito_tokens_command(message:Message):
    capy = Capybara_Controller(message)
    print(f"➡️ Пользователь {capy.usern} написал команду /papito_tokens")
    result, success = capy.get_papito_tokens(message)
    if success == 'No_capy' or not success:
        await message.answer('❌ У тебя нет капибары! Создай командой /capybara')
    else:
        await message.answer(result)


@router.message(Command('shop'))
async def shop_command(message:Message):
    capy = Capybara_Controller(message)
    print(f"➡️ Пользователь {capy.usern} написал команду /shop")
    button1 = InlineKeyboardButton(
        text="🍎 Яблоко - 50 🪙",
        callback_data="buy_1"
    )

    button2 = InlineKeyboardButton(
        text="🍉 Арбуз - 100 🪙",
        callback_data="buy_2"
    )

    button3 = InlineKeyboardButton(
        text="🎲 Лотерея - 25 🪙",
        callback_data="buy_3"
    )

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [button1, button2],
        [button3]             
    ])
    await message.answer("🛒 **МАГАЗИН ДЛЯ КАПИБАРЫ** 🛒\n\nВыбери товар:\n🍎 Яблоко - Ты сможешь кормить капибару на 1 минуту раньше\n🍉 Арбуз - 2 уровня сразу\n🎲 Лотерея - от 1 до 100 папито токенов", 
                     reply_markup=keyboard, 
                     parse_mode="Markdown")
    
    capy.close()

@router.callback_query(lambda c:c.data == 'buy_1')
async def buy1_command(callback : callback_query):

    class FakeMessage:
        from_user = callback.from_user

    fakemessage = FakeMessage()
    capy = Capybara_Controller(fakemessage)
    print(f"➡️ Пользователь {capy.usern} нажал кнопку: Яблоко")


    result,succsess = capy.purchase_item(fakemessage,1)
    
    if succsess == 'No_capy':
        await callback.answer('❌ У тебя нет капибары! Создай командой /capybara')
    else:
        await callback.message.answer(result)
        await callback.answer()
    capy.close()




@router.callback_query(lambda c:c.data == 'buy_2')
async def buy2_command(callback : callback_query):

    class FakeMessage:
        from_user = callback.from_user

    fakemessage = FakeMessage()
    capy = Capybara_Controller(fakemessage)
    print(f"➡️ Пользователь {capy.usern} нажал кнопку: Яблоко")


    result,succsess = capy.purchase_item(fakemessage,2)
    
    if succsess == 'No_capy':
        await callback.answer('❌ У тебя нет капибары! Создай командой /capybara')
    else:
        await callback.message.answer(result)
        await callback.answer()
    capy.close()


@router.callback_query(lambda c:c.data == 'buy_3')
async def buy3_command(callback : callback_query):

    class FakeMessage:
        from_user = callback.from_user

    fakemessage = FakeMessage()
    capy = Capybara_Controller(fakemessage)
    print(f"➡️ Пользователь {capy.usern} нажал кнопку: Яблоко")


    result,succsess = capy.purchase_item(fakemessage,3)
    
    if succsess == 'No_capy':
        await callback.answer('❌ У тебя нет капибары! Создай командой /capybara')
    else:
        await callback.message.answer(result)
        await callback.answer()
    capy.close()
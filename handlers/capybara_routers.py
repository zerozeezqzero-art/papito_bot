#aio
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import FSInputFile,InlineKeyboardButton,InlineKeyboardMarkup,Message,callback_query


#modules import
from controller import Capybara_Controller
from logging_bot import log_to_file
from logging_bot import try_ex_deco

#lib
import random


router = Router()





@router.message(Command('capybara'))
@try_ex_deco
async def capybara_command_create(message:Message):
    capy = Capybara_Controller(message)
    
    log_to_file(f"➡️ Пользователь {capy.usern} написал команду /capybara")
    
    if capy.create_capy():
        await message.answer_photo(FSInputFile(capy.images['capy_born']),caption=f'КАПИБАРА {capy.usern} СОЗДАНА!')
        capy.close()
    else:
        await message.answer('У ВАС УЖЕ ЕСТЬ КАПИБАРА!')
        capy.close()



@router.message(Command('capyfeed'))
@try_ex_deco
async def capybara_command_feed(message:Message):
    capy = Capybara_Controller(message)
    log_to_file(f"➡️ Пользователь {capy.usern} написал команду /capyfeed")
    
    if capy.is_troll_mode(message.from_user.username):
        if random.randint(0, 1) == 0:
            await message.answer('ОШИБКА!❌')
            capy.close()
            return
        else:
            pass
    result, success = capy.feed_capy(message)
    
    
    if result is None:
        await message.answer('❌ У тебя нет капибары! Создай командой /capybara')
        capy.close()
        return
    
    if success:
        await message.answer_photo(FSInputFile(capy.images['capy_pokormlena']),caption=result)
    else:
        await message.answer_photo(FSInputFile(capy.images['capy_eat']), caption=result)
    
    capy.close()



@router.message(Command('capylevel'))
@try_ex_deco
async def capybara_command_level(message:Message):
    capy = Capybara_Controller(message)
    log_to_file(f"➡️ Пользователь {capy.usern} написал команду /capylevel")
    
    if capy.is_troll_mode(message.from_user.username):
        if random.randint(0, 1) == 0:
            await message.answer('ОШИБКА!❌')
            capy.close()
            return
        else:
            pass
    lvl, success = capy.get_capy_level(message)
    if success == 'No_capy' or not success:
        await message.answer('❌ У тебя нет капибары! Создай командой /capybara')
    else:
        await message.answer(f'Уровень вашей капибары - {lvl}')
    capy.close()



@router.message(Command('leaderboard'))
async def leaderboard_command(message:Message):
    capy = Capybara_Controller(message)
    log_to_file(f"➡️ Пользователь {capy.usern} написал команду /leaderboard")
    
    if capy.is_troll_mode(message.from_user.username):
        if random.randint(0, 1) == 0:
            await message.answer('ОШИБКА!❌')
            capy.close()
            return
        else:
            pass
    
    result = capy.leaderboard()
    await message.answer_photo(FSInputFile(capy.images['capy_leader_board']),caption=result)
    capy.close()


@router.message(Command('photo'))
@try_ex_deco
async def capybara_photo_command(message:Message):
    capy = Capybara_Controller(message)
    log_to_file(f"➡️ Пользователь {capy.usern} написал команду /photo")
    
    if capy.is_troll_mode(message.from_user.username):
        if random.randint(0, 1) == 0:
            await message.answer('ОШИБКА!❌')
            capy.close()
            return
        else:
            pass
    
    copibara = FSInputFile(random.choice(capy.images['random_capy']))
    await message.answer_photo(copibara, caption="вот и твоя капибара...")
    capy.close()



@router.message(Command('papito_tokens'))
@try_ex_deco
async def papito_tokens_command(message:Message):
    capy = Capybara_Controller(message)
    log_to_file(f"➡️ Пользователь {capy.usern} написал команду /papito_tokens")
    
    if capy.is_troll_mode(message.from_user.username):
        if random.randint(0, 1) == 0:
            await message.answer('ОШИБКА!❌')
            capy.close()
            return
        else:
            pass
    
    result, success = capy.get_papito_tokens(message)
    if success == 'No_capy' or not success:
        await message.answer('❌ У тебя нет капибары! Создай командой /capybara')
    else:
        await message.answer(result)


@router.message(Command('shop'))
@try_ex_deco
async def shop_command(message:Message):
    capy = Capybara_Controller(message)
    log_to_file(f"➡️ Пользователь {capy.usern} написал команду /shop")
    if capy.is_troll_mode(message.from_user.username):
        if random.randint(0, 1) == 0:
            await message.answer('ОШИБКА!❌')
            capy.close()
            return
        else:
            pass
    
    
    
    button1 = InlineKeyboardButton(
        text="🍎 Яблоко - 50 🪙",
        callback_data="buy_1"
    )

    button2 = InlineKeyboardButton(
        text="🍉 Арбуз - 100 🪙",
        callback_data="buy_2"
    )

    button3 = InlineKeyboardButton(
        text="🎲 Лотерея - 45 🪙",
        callback_data="buy_3"
    )

    button4 = InlineKeyboardButton(
        text="🎣 Обычная - 100 🪙",
        callback_data="buy_4"
    )

    button5 = InlineKeyboardButton(
        text="🎣 Эпическая - 500  🪙",
        callback_data="buy_5"
    )


    button6 = InlineKeyboardButton(
        text="🎣 Легендарная - 1000  🪙",
        callback_data="buy_6"
    )

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [button1, button2,button3],
        [button4,button5],
        [button6]   
    ])
    await message.answer_photo(
        FSInputFile(capy.images['capy_shop']),
        caption="🛒 **МАГАЗИН ДЛЯ КАПИБАРЫ** 🛒\n\n"
                "Выбери товар:\n"
                "🍎 Яблоко - Ты сможешь кормить капибару на 1 минуту раньше\n"
                "🍉 Арбуз - 2 уровня сразу\n"
                "🎲 Лотерея - от 1 до 100 папито токенов\n"
                "🎣 Обычная удочка - разблокирует рыбалку\n"
                "🎣 Эпическая удочка - шанс на редкую рыбу\n"
                "🎣 Легендарная удочка - шанс на легендарную рыбу", 
        reply_markup=keyboard, 
        parse_mode="Markdown"
    )
    capy.close()


@router.callback_query(lambda c:c.data == 'buy_1')
@try_ex_deco
async def buy1_command(callback : callback_query):

    class FakeMessage:
        from_user = callback.from_user

    fakemessage = FakeMessage()
    capy = Capybara_Controller(fakemessage)
    log_to_file(f"➡️ Пользователь {capy.usern} нажал кнопку: Яблоко")


    result,succsess = capy.purchase_item(fakemessage,1)
    
    if succsess == 'No_capy':
        await callback.answer('❌ У тебя нет капибары! Создай командой /capybara')
    else:
        await callback.message.answer(result)
        await callback.answer()
    capy.close()




@router.callback_query(lambda c:c.data == 'buy_2')
@try_ex_deco
async def buy2_command(callback : callback_query):

    class FakeMessage:
        from_user = callback.from_user

    fakemessage = FakeMessage()
    capy = Capybara_Controller(fakemessage)
    log_to_file(f"➡️ Пользователь {capy.usern} нажал кнопку: Арбуз")


    result,succsess = capy.purchase_item(fakemessage,2)
    
    if succsess == 'No_capy':
        await callback.answer('❌ У тебя нет капибары! Создай командой /capybara')
    else:
        await callback.message.answer(result)
        await callback.answer()
    capy.close()


@router.callback_query(lambda c:c.data == 'buy_3')
@try_ex_deco
async def buy3_command(callback : callback_query):

    class FakeMessage:
        from_user = callback.from_user

    fakemessage = FakeMessage()
    capy = Capybara_Controller(fakemessage)
    log_to_file(f"➡️ Пользователь {capy.usern} нажал кнопку: Лотерея")


    result,succsess = capy.purchase_item(fakemessage,3)
    
    if succsess == 'No_capy':
        await callback.answer('❌ У тебя нет капибары! Создай командой /capybara')
    else:
        await callback.message.answer(result)
        await callback.answer()
    capy.close()



@router.callback_query(lambda c:c.data == 'buy_4')
@try_ex_deco
async def buy4_command(callback : callback_query):

    class FakeMessage:
        from_user = callback.from_user

    fakemessage = FakeMessage()
    capy = Capybara_Controller(fakemessage)
    log_to_file(f"➡️ Пользователь {capy.usern} нажал кнопку: Обычная удочка")
    result,succsess = capy.purchase_item(fakemessage,4)
    
    if succsess == 'No_capy':
        await callback.answer('❌ У тебя нет капибары! Создай командой /capybara')
    else:
        await callback.message.answer(result)
        await callback.answer()
    capy.close()




@router.callback_query(lambda c:c.data == 'buy_5')
@try_ex_deco
async def buy5_command(callback : callback_query):

    class FakeMessage:
        from_user = callback.from_user

    fakemessage = FakeMessage()
    capy = Capybara_Controller(fakemessage)
    log_to_file(f"➡️ Пользователь {capy.usern} нажал кнопку: Эпическая удочка")


    result,succsess = capy.purchase_item(fakemessage,5)
    
    if succsess == 'No_capy':
        await callback.answer('❌ У тебя нет капибары! Создай командой /capybara')
    else:
        await callback.message.answer(result)
        await callback.answer()
    capy.close()




@router.callback_query(lambda c:c.data == 'buy_6')
@try_ex_deco
async def buy6_command(callback : callback_query):

    class FakeMessage:
        from_user = callback.from_user

    fakemessage = FakeMessage()
    capy = Capybara_Controller(fakemessage)
    log_to_file(f"➡️ Пользователь {capy.usern} нажал кнопку: Легендарная удочка")

    result,succsess = capy.purchase_item(fakemessage,6)
    
    if succsess == 'No_capy':
        await callback.answer('❌ У тебя нет капибары! Создай командой /capybara')
    else:
        await callback.message.answer(result)
        await callback.answer()
    capy.close()



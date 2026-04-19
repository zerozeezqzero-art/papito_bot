from aiogram import Router
from aiogram.types import Message,FSInputFile
from aiogram.filters import Command
from PIL import Image
from controller import Capybara_Controller


router = Router()

@router.message(Command('byst'))
async def start_command(message: Message):
    capy = Capybara_Controller(message)
    if message.photo:
        photo = message.photo[-1]
        file = await message.bot.get_file(photo.file_id)
        filepath = f"byst_kartinok/{photo.file_id}_{capy.usern}.jpg"
        '''SAVE PHOTO'''
        
        await message.bot.download_file(file.file_path, filepath)
        
        '''byst'''
        img = Image.open(filepath)
        img.save(filepath, quality=3)
        img.close()

        await message.answer_photo(FSInputFile(filepath), caption='Фото забущено')
        
    else:
        await message.answer("❌ Отправь фото с командой /byst")
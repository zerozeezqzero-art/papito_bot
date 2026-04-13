import cv2
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

router = Router()

@router.message(Command('byst'))
async def start_command(message: Message):
    
    img = cv2.imread("input.png")
    img = cv2.GaussianBlur(img, (11, 11), 0)

    cv2.imwrite("output.png", img)

    await message.answer_photo(photo=open("output.png", "rb"))


"""ДОДЕЛАТЬ ПОТОМ!!! БУСТ КАРТИНОК ОПЕН ЦИВИ"""
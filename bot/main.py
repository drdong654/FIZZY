import asyncio
import os

from aiogram import Bot, Dispatcher, F, Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message
from aiogram.types import FSInputFile
from dotenv import load_dotenv

from bot.keyboard import main_keyboard


load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise ValueError("No no BOT_TOKEN provided. Please set the BOT_TOKEN environment variable")

router = Router()

@router.message(Command("start"))
async def show_start(message: Message):
    photo = FSInputFile("media/mascots/fizzy-owl-mascot.png")
    reply_markup = main_keyboard

    await message.answer_photo(
        photo=photo,
        caption=(
            "Hello, dear friend! I'm ChatBot for social listening.\n"
            "Use the buttons below👇\n"
            "or type /help to get more information."
        ),
        reply_markup=reply_markup,

    )

#Добавляем команду start и кнопку Start
@router.message(Command("start"))
async def start_command(message: Message):
    await show_start(message)


@router.message(F.text == "Start")
async def start_button(message: Message):
    await show_start(message)

@router.message(Command("help"))
async def help_command(message: Message):
    await message.answer(
        "Доступные команды:\n"
        "/start - начать работу с ботом\n"
        "/help - получить помощь\n"
    )
@router.message(F.text == "Help")
async def help_button(message: Message):
    await help_command(message)

async def main():
    bot = Bot(token=TOKEN)
    dispatcher = Dispatcher()

    dispatcher.include_router(router)

    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
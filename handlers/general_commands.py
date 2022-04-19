from aiogram import types
from misc import *
import keyboard
import funk


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.answer('Выберите и нажмите на кнопку ниже.', reply_markup=keyboard.menu_start())

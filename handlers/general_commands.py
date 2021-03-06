from email import message
from aiogram import types
from click import command
from misc import *
import keyboard
import funk
from asyncio import sleep


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply('Отлично! Здесь вы сможете вести переписку с нашим менеджером и иметь быстрый доступ ко всем ссылкам.', reply_markup=keyboard.main())
    await sleep(1)
    await message.answer('Выберите и нажмите на кнопку ниже.', reply_markup=keyboard.menu_start())


@dp.message_handler(commands=['main'], state='*')
async def stop_chatting(message: types.Message, state: FSMContext):
    await message.answer('Выберите и нажмите на кнопку ниже.', reply_markup=keyboard.menu_start())
    await state.finish()

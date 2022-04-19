import logging
from aiogram import Bot, Dispatcher
from config import TOKEN
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

storage = MemoryStorage()


class Form(StatesGroup):
    callme = State()
    feedback = State()


bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)
logging.basicConfig(level=logging.INFO)

import logging
import os

from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv
from api import user_methods


load_dotenv()

logging.basicConfig(level=logging.INFO)

bot = Bot(token=os.getenv('API_TOKEN'))
print(os.getenv('API_TOKEN'))
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def send_welocome(message: types.Message):
    await message.reply('WOWOWOW HI')


@dp.message_handler()
async def log(message: types.Message):
    if message.text.lower() == 'Show users':
        print(await user_methods.get_users())
    
    elif message.text.lower() == 'add me':
        user_id = message['from']['id']
        username = message['from']['username']
        nickname = message['from']['first_name']
        await user_methods.add_user(id=user_id, username=username,
                                    nickname=nickname)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

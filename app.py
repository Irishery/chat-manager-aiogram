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

async def user_in_db(id):
    user = await user_methods.get_user(id, 'telegram')
    if user:
        return True
    return False


@dp.message_handler(commands=['start'])
async def send_welocome(message: types.Message):
    await message.reply('WOWOWOW HI')


@dp.message_handler()
async def log(message: types.Message):
    user_id = message['from']['id']
    username = message['from']['username']
    nickname = message['from']['first_name']
    text = message.text

    if not await user_in_db(user_id):
        await user_methods.add_user(id=user_id, username=username,
                                    nickname=nickname)

    await user_methods.send_message(id=user_id, text=text,
                                        nickname=nickname)

    if message.text.lower() == 'show users':
        print(await user_methods.get_users())


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

from base64 import encodebytes
import logging
import os

from threading import Thread
from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv
from api import user_methods
from api.msgs_handler import msgs_handler


load_dotenv()

logging.basicConfig(level=logging.INFO)

bot = Bot(token=os.getenv('API_TOKEN'))
print(os.getenv('API_TOKEN'))
dp = Dispatcher(bot)

async def user_in_db(id):
    user = await user_methods.get_user(id, 'telegram')
    
    if user:
        if user['is_banned']:
            return 'banned'
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

    check_user = await user_in_db(user_id)
    if not check_user or check_user == 'banned':
        if check_user == 'banned':
            return await bot.send_message(user_id, 'Вы забанены)')
        await user_methods.add_user(id=user_id, username=username,
                                    nickname=nickname)
        user_photos = await bot.get_user_profile_photos(user_id, limit=1)
        if user_photos['total_count']:
            file_id = user_photos['photos'][0][0]['file_id']
            file = await bot.get_file(file_id)
            file_path = file.file_path
            image = await bot.download_file(file_path)
            im_b64 = encodebytes(image.read()).decode("utf-8")
            await user_methods.send_pic(im_b64, {'telegram_id': user_id})

    await user_methods.send_message(id=user_id, text=text,
                                        nickname=nickname)

    if message.text.lower() == 'show users':
        print(await user_methods.get_users())


if __name__ == '__main__':

    therad = Thread(target=msgs_handler.run, kwargs={'host': '127.0.0.1',
                                                     'port': 8181, 
                                                     'debug': True,
                                                     'use_reloader': False})
    therad.start()
    executor.start_polling(dp, skip_updates=True)

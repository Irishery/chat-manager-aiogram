import logging
import os
import asyncio

from asyncio import new_event_loop, set_event_loop, get_event_loop
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

async def on_startup(_):
    await asyncio.create_task(msgs_handler.run(host="127.0.0.1", port=8181))


if __name__ == '__main__':
    # set_event_loop(new_event_loop())
    # thread = Thread(target=executor.start_polling, args=(dp,),
                    # kwargs={'skip_updates': True})
    # thread.start()
    therad = Thread(target=msgs_handler.run, kwargs={'host': '127.0.0.1',
                                                     'port': 8181, 
                                                     'debug': True,
                                                     'use_reloader': False})
    therad.start()
    # loop = get_event_loop()
    # loop.create_task(msgs_handler.run(host="127.0.0.1", port=8181))
    executor.start_polling(dp, skip_updates=True)
    # msgs_handler.run()

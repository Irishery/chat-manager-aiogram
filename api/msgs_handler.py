import os

from dotenv import load_dotenv
from flask import Flask, request
from aiogram import Bot
from handlers.manager_chat import users_in_chat
import keyboard

load_dotenv()

bot = Bot(token=os.getenv('API_TOKEN'))

msgs_handler = Flask(__name__)

@msgs_handler.route('/send_message/', methods=['POST'])
async def post_message():
    data = request.args.to_dict()
    if data['telegram_id'] not in users_in_chat.keys():
        await bot.send_message(data['telegram_id'], 'Чтобы ответить менеджеру, нажмите на кнопку "Написать нам"', reply_markup=keyboard.first_msg())
    await bot.send_message(data['telegram_id'],
                        data["message_text"])
    return {'status': 'ok'}

import os

from dotenv import load_dotenv
from flask import Flask, request
from aiogram import Bot

load_dotenv()

bot = Bot(token=os.getenv('API_TOKEN'))

msgs_handler = Flask(__name__)

@msgs_handler.route('/send_message/', methods=['POST'])
async def post_message():
    data = request.args.to_dict()
    await bot.send_message(data['telegram_id'],
                        data["message_text"])
    return {'status': 'ok'}

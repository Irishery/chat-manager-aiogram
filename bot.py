from aiogram import executor
from misc import dp
from api.msgs_handler import msgs_handler
from threading import Thread
import handlers

if __name__ == "__main__":

    therad = Thread(target=msgs_handler.run, kwargs={'host': '127.0.0.1',
                                                    'port': 8181, 
                                                    'debug': True,
                                                    'use_reloader': False})
    therad.start()
    executor.start_polling(dp, skip_updates=True)

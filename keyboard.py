from aiogram import types
import funk


def menu_start():
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(types.InlineKeyboardButton(text='📢 Наши медиа', callback_data='menu_media'))
    keyboard.add(types.InlineKeyboardButton(text='📄 Отзывы после обучения', callback_data='menu_review'))
    keyboard.add(
        types.InlineKeyboardButton(text='🎓 Перейти в академию', url="https://tt.academy?utm_source=reviewbot"))
    keyboard.add(types.InlineKeyboardButton(text='📩 Написать нам', callback_data='feedback'))
    keyboard.add(types.InlineKeyboardButton(text='📞 Запросить звонок', callback_data='callme_name'))
    return keyboard


def menu_media():
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(types.InlineKeyboardButton(text='📺 YouTube', url="https://www.youtube.com/c/TopTradersAcademy"))
    keyboard.add(types.InlineKeyboardButton(text='🏆 Телеграм канал ТТ', url="https://t.me/toptradingview"))
    keyboard.add(types.InlineKeyboardButton(text='🎓 Телеграм канал ТТА', url="https://t.me/tt_academy"))
    keyboard.add(types.InlineKeyboardButton(text='🦄 Телеграм канал DeFiLog', url="https://t.me/DeFiLoG"))
    keyboard.add(types.InlineKeyboardButton(text='🕊 Twitter TT', url="https://twitter.com/TopTradersbyTV"))
    keyboard.add(types.InlineKeyboardButton(text='Instagram TTA', url="https://www.instagram.com/toptraders_academy"))
    keyboard.add(types.InlineKeyboardButton(text='Facebook TTA', url="https://www.facebook.com/toptradersacademy"))
    keyboard.add(types.InlineKeyboardButton(text='Medium', url="https://medium.com/@toptradersico"))
    keyboard.add(
        types.InlineKeyboardButton(text='Yandex Dzen', url="https://zen.yandex.ru/id/60127ba261648604d19a9648"))
    keyboard.add(types.InlineKeyboardButton(text='VC Blog', url="https://vc.ru/u/642470-top-traders"))
    keyboard.add(types.InlineKeyboardButton(text='⬅️ Назад', callback_data='menu_back'))
    return keyboard


def menu_review():
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(types.InlineKeyboardButton(text="Crypto Camp", callback_data="option;1"))
    keyboard.add(types.InlineKeyboardButton(text="Crypto Basics", callback_data="option;2"))
    keyboard.add(types.InlineKeyboardButton(text="Антихаос", callback_data="option;3"))
    keyboard.add(types.InlineKeyboardButton(text="DayTrading Futures", callback_data="option;4"))
    keyboard.add(types.InlineKeyboardButton(text="DeFi", callback_data="option;5"))
    keyboard.add(types.InlineKeyboardButton(text="Инсайт", callback_data="option;6"))
    keyboard.add(types.InlineKeyboardButton(text="⬅️ Наaзад", callback_data="menu_back"))
    return keyboard


def menu_back():
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(types.InlineKeyboardButton(text='⬅️ Главное меню', callback_data='main_menu'))
    return keyboard


def pagination(number, len_rew, number_file_read, prew, pag=True):
    if pag:
        keyboard = types.InlineKeyboardMarkup(row_width=5)
        numbers = funk.number_button(number)
        row = []
        row.append(types.InlineKeyboardButton(text="<", callback_data=f"prew_post;{number};{number_file_read};{prew}"))
        for i in range(len_rew):
            if int(numbers[i]) == int(prew):
                row.append(types.InlineKeyboardButton(text=str(numbers[i]),
                                                      callback_data='ignore'))
            else:
                row.append(types.InlineKeyboardButton(text=str(numbers[i]),
                                                      callback_data=f'see_rew;{numbers[i]};{number};{number_file_read};{prew}'))

        row.append(types.InlineKeyboardButton(text=">", callback_data=f"next_post;{number};{number_file_read};{prew}"))
        keyboard.row(*row)
        row = [types.InlineKeyboardButton(text='⬅️ Назад',
                                          callback_data='review_back')]
        keyboard.row(*row)
    else:
        keyboard = types.InlineKeyboardMarkup()
        row = []
        numbers = [1, 2, 3]

        for i in range(len_rew):
            if int(numbers[i]) == int(prew):
                row.append(types.InlineKeyboardButton(text=str(numbers[i]),
                                                      callback_data='ignore'))
            else:
                row.append(types.InlineKeyboardButton(text=str(numbers[i]),
                                                      callback_data=f'see_rew;{numbers[i]};{number};{number_file_read};{prew}'))
        keyboard.row(*row)
        keyboard.add(types.InlineKeyboardButton(text='⬅️ Назад',
                                                callback_data='review_back'))

    return keyboard


def number_request():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    button = types.KeyboardButton("Поделиться номером", request_contact=True)
    keyboard.add(button)
    return keyboard


def add_reviews(number):
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    row = [types.InlineKeyboardButton(text='✅ Опубликовать', callback_data=f'add_rew;{number}')]
    row.append(types.InlineKeyboardButton(text='❌ Отклонить', callback_data='del_rew'))
    keyboard.row(*row)
    return keyboard


def chat_state():
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    row = [types.InlineKeyboardButton(text='Назад', callback_data='stop_chatting')]
    keyboard.row(*row)
    return keyboard


def call_state():
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    row = [types.InlineKeyboardButton(text='Отменить', callback_data='stop_call')]
    keyboard.row(*row)
    return keyboard


def main():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    row = types.KeyboardButton(text='Главная', callback_data='stop_chatting')
    keyboard.row(row)
    return keyboard


def first_msg():
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    row = [types.InlineKeyboardButton(text='Продолжить общение', callback_data='feedback_manager_first')]
    keyboard.row(*row)
    return keyboard

from aiogram import types
from misc import *
import keyboard
from config import ADMIN

@dp.message_handler(content_types=types.ContentType.PHOTO)
async def photo_step(message):
    photo_id = message.photo[-1].file_id
    await message.answer(photo_id)


@dp.message_handler(content_types=types.ContentType.TEXT)
async def text_step(message):
    id_user = (str(message.from_user.id))
    if message.text[:4] == 'post':
        id_foto = message.text.split()[-1]
        txt = message.text[6:-len(id_foto)]
        try:
            await bot.send_photo(id_user, id_foto, caption=txt, reply_markup=keyboard.add_reviews(message.text[4]))
        except:
            await message.answer('неправильный ID картинки')
    if message.text[:4] == 'Имя:':
        txt = message.text
        print(txt)
    else:
        await bot.delete_message(id_user, message_id=message.message_id)


@dp.message_handler(state=Form.callme)
async def process_call(message: types.Message, state: FSMContext):
    user = types.User.get_current()
    async with state.proxy() as data:
        data['text'] = message.text
        data['fname'] = user['first_name']
        data['uname'] = user['username']
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(types.InlineKeyboardButton(text='Изменить', callback_data='callme'))
    markup.add(types.InlineKeyboardButton(text='Отправить', callback_data='sendtogroup'))
    await message.reply("Внимательно проверьте вашу заявку перед отправкой", reply_markup=markup)

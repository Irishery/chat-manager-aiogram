from aiogram import types
from misc import *
import keyboard
import phonenumbers
from config import ADMIN

call_requests = {}


@dp.message_handler()
async def main_page_filter(message: types.Message, state: FSMContext):
    id_user = (str(message.from_user.id))

    if message.text == 'Главная' or message.text == '/start':
        await message.answer('Выберите и нажмите на кнопку ниже!', reply_markup=keyboard.menu_start())
        await state.finish()
        return

    await bot.delete_message(id_user, message_id=message.message_id)


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


@dp.message_handler(content_types=['contact'], state=Form.callme_number)
async def contact_handler(message,  state: FSMContext):
    print(message.contact.phone_number)
    id_user = (str(message.from_user.id))
    if id_user in call_requests.keys():
        call_requests[id_user]['contact'] = message.contact.phone_number
    else:
        call_requests[id_user] = {'contact': f'{message.contact.phone_number}', 'name': '', 'subject': ''}
    
    await message.answer('Спасибо. И последнее: по какому вопросу/теме обращаетесь?', reply_markup=keyboard.main())
    await Form.callme_subject.set()


@dp.message_handler(content_types=['text'], state=Form.callme_number)
async def contact_handler_text(message: types.Message, state: FSMContext):
    id_user = (str(message.from_user.id))
    if message.text == 'Главная' or message.text == '/start':
        await message.answer('Запрос отменен', reply_markup=keyboard.main())
        await message.answer('Выберите и нажмите на кнопку ниже!', reply_markup=keyboard.menu_start())
        await state.finish()
        return
    try:
        number = phonenumbers.parse(message.text)
    except phonenumbers.NumberParseException:
        return await message.answer('Пожалуйста, введите правильный номер телефона в международном формате (например, +74959883345)')

    if phonenumbers.is_valid_number(number):
        if id_user in call_requests.keys():
            call_requests[id_user]['contact'] = message.text
        else:
            call_requests[id_user] = {'contact': f'{message.text}', 'name': '', 'subject': ''}

        await message.answer('Спасибо. И последнее: по какому вопросу/теме обращаетесь?', reply_markup=keyboard.main())
        await Form.callme_subject.set()

    else:
        return await message.answer('Пожалуйста, введите правильный номер телефона в международном формате (например, +74959883345)')

#@dp.message_handler(state=Form.callme)
#async def process_call(message: types.Message, state: FSMContext):
#    user = types.User.get_current()
#    print(message)
#    async with state.proxy() as data:
#        data['text'] = message.text
#        data['fname'] = user['first_name']
#        data['uname'] = user['username']
#    markup = types.InlineKeyboardMarkup(row_width=2)
#    markup.add(types.InlineKeyboardButton(text='Изменить', callback_data='callme'))
#    markup.add(types.InlineKeyboardButton(text='Отправить', callback_data='sendtogroup'))
#    await message.reply("Внимательно проверьте вашу заявку перед отправкой", reply_markup=markup)

@dp.message_handler(state=Form.callme_name)
async def get_name(message: types.Message, state: FSMContext):
    user = types.User.get_current()
    if message.text == 'Главная' or message.text == '/start':
        await message.answer('Выберите и нажмите на кнопку ниже!', reply_markup=keyboard.menu_start())
        await state.finish()
        return
    id_user = (str(message.from_user.id))
    print(message.text)
    if id_user in call_requests.keys():
        call_requests[id_user]['name'] = message.text
    else:
        call_requests[id_user] = {'contact': '', 'name': f'{message.text}', 'subject': ''}
    print(call_requests)
    await message.answer('Отлично. Оставьте нам свой номер телефона, чтобы мы с вами связались.', reply_markup=keyboard.number_request())
    await Form.callme_number.set()


@dp.message_handler(state=Form.callme_subject)
async def get_subject(message: types.Message, state: FSMContext):
    if message.text == 'Главная' or message.text == '/start':
        await message.answer('Выберите и нажмите на кнопку ниже!', reply_markup=keyboard.menu_start())
        await state.finish()
        return
    user = types.User.get_current()
    id_user = (str(message.from_user.id))
    if id_user in call_requests.keys():
        call_requests[id_user]['subject'] = message.text
    else:
        call_requests[id_user] = {'contact': '', 'name': '', 'subject': f'{message.text}'}

    async with state.proxy() as data:
        print(call_requests[f"{user.id}"]["name"])
        data['text'] = f'Имя: {call_requests[f"{user.id}"]["name"]}\nТелефон: {call_requests[f"{user.id}"]["contact"]}\nТема: {call_requests[f"{user.id}"]["subject"]}'
        data['fname'] = user['first_name']
        data['uname'] = user['username']
        data['contact'] = call_requests[str(user.id)]["contact"]
        data['name'] = call_requests[str(user.id)]["name"]
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(types.InlineKeyboardButton(text='Изменить', callback_data='callme_name'))
    markup.add(types.InlineKeyboardButton(text='Отправить', callback_data='sendtogroup'))
    await message.reply(f'Внимательно проверьте вашу заявку перед отправкой\nИмя: {call_requests[f"{user.id}"]["name"]}\nТелефон: {call_requests[f"{user.id}"]["contact"]}\nТема: {call_requests[f"{user.id}"]["subject"]}', reply_markup=markup)

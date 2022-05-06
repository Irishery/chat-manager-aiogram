from aiogram import types
from misc import *
from base64 import encodebytes
from api import user_methods
import keyboard

users_in_chat = {}

async def user_in_db(id):
    user = await user_methods.get_user(id, 'telegram')
    
    if user:
        if user['is_banned']:
            return 'banned'
        return True
    return False


@dp.message_handler(state=Form.feedback)
async def log(message: types.Message, state: FSMContext):
    user_id = message['from']['id']
    username = message['from']['username']
    nickname = message['from']['first_name']
    text = message.text
    print(users_in_chat.keys())

    try:
        if users_in_chat[str(user_id)] == 2:
            users_in_chat[str(user_id)] = True
            if message.text not in ['Главная', '/start']:
                await message.answer('_Спасибо, мы приняли вашу заявку. Ожидайте ответ здесь в боте._', parse_mode="Markdown")
    except KeyError:
        users_in_chat[str(user_id)] = True

    if text == 'Главная' or text == '/start':
        users_in_chat.pop(str(user_id))
        await state.finish()
        await message.answer('_Чат прерван. Чтобы опять связаться с нашим менеджером, нажмите кнопку «Написать нам»._', parse_mode="Markdown")
        await message.answer('Выберите и нажмите на кнопку ниже!', reply_markup=keyboard.menu_start())
    print('checking user in db')
    check_user = await user_in_db(user_id)
    print('checked')
    if not check_user or check_user == 'banned':
        print('not in db or banned')
        if check_user == 'banned':
            print('user is banned')
            return await bot.send_message(user_id, 'Вы забанены')
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
    print(message['from'])

    await user_methods.send_message(id=user_id, text=text,
                                        nickname=nickname, is_call=False)

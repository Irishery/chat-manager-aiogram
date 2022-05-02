from aiogram import types
from misc import *
from .manager_chat import users_in_chat
import csv
import funk
import keyboard
from api import user_methods


users = []
msgs_to_del = {}


@dp.callback_query_handler(state="*")
async def callback_btn(call: types.CallbackQuery, state: FSMContext):
    id_user = str(call.message.chat.id)
    data = call.data.split(";")

    if data[0] == "del_rew":
        await bot.delete_message(id_user, message_id=call.message.message_id)

    elif data[0] == "add_rew":
        number_file_write = data[1]
        file_id = call.message.photo[-1].file_id
        caption = call.message.caption
        try:
            funk.add_post(file_id, caption, number_file_write)
        except:
            funk.write_new_post(file_id, caption, number_file_write)
        await bot.delete_message(id_user, message_id=call.message.message_id)
        await call.message.answer('Готово')
        await call.answer()

    elif data[0] == "next_post":
        next = int(data[1])
        all_reviews = funk.see_rew(data[2])
        reviews = funk.sort_reviews(all_reviews)
        rev = funk.see_rew(data[2])[int(data[1]) - 1]
        if len(reviews) == next + 1:
            number = 0
        else:
            number = next + 1
        await bot.edit_message_reply_markup(call.message.chat.id,
                                            call.message.message_id,
                                            reply_markup=keyboard.pagination(number=number,
                                                                             len_rew=len(reviews[number]),
                                                                             number_file_read=data[2],
                                                                             prew=data[3]))

    elif data[0] == "menu_media":
        await bot.edit_message_reply_markup(call.message.chat.id,
                                            call.message.message_id,
                                            reply_markup=keyboard.menu_media())

    elif data[0] == "review_back":
        await bot.delete_message(id_user, message_id=call.message.message_id)
        await call.message.answer(
            'Выберите и нажмите на кнопку ниже!',
            reply_markup=keyboard.menu_review())
        await call.answer()

    elif data[0] == "menu_review":
        await bot.edit_message_reply_markup(call.message.chat.id,
                                            call.message.message_id,
                                            reply_markup=keyboard.menu_review())

    elif data[0] == "menu_back":
        await bot.edit_message_reply_markup(call.message.chat.id,
                                            call.message.message_id,
                                            reply_markup=keyboard.menu_start())

    elif data[0] == "prew_post":
        next = int(data[1])
        all_reviews = funk.see_rew(data[2])
        reviews = funk.sort_reviews(all_reviews)
        rev = funk.see_rew(data[2])[int(data[1]) - 1]
        if next == 0:
            number = len(reviews) - 1
        else:
            number = next - 1
        await bot.edit_message_reply_markup(call.message.chat.id,
                                            call.message.message_id,
                                            reply_markup=keyboard.pagination(number=number,
                                                                             len_rew=len(reviews[number]),
                                                                             number_file_read=data[2],
                                                                             prew=data[3]))

    elif data[0] == "see_rew":
        number_file_read = data[3]
        all_reviews = funk.see_rew(number_file_read)
        reviews = funk.sort_reviews(all_reviews)
        rev = funk.see_rew(number_file_read)[int(data[1]) - 1]
        len_rew = len(reviews[int(data[2])])
        if len(all_reviews) <= 3:
            await bot.edit_message_media(types.InputMediaPhoto(rev[0], rev[1]), call.message.chat.id,
                                         call.message.message_id,
                                         reply_markup=keyboard.pagination(number=int(data[2]),
                                                                          number_file_read=number_file_read,
                                                                          len_rew=len_rew,
                                                                          prew=data[1],
                                                                          pag=False))
        else:

            await bot.edit_message_media(types.InputMediaPhoto(rev[0], rev[1]), call.message.chat.id,
                                         call.message.message_id,
                                         reply_markup=keyboard.pagination(number=int(data[2]),
                                                                          len_rew=len_rew,
                                                                          number_file_read=number_file_read,
                                                                          prew=data[1],

                                                                          ))
        await call.answer()

    elif data[0] == "option":
        print(data)
        number_file_read = data[1]
        try:
            pag = True
            all_reviews = funk.see_rew(number_file_read)
            rev = all_reviews[0]
            reviews = funk.sort_reviews(all_reviews)
            print('ok3')
            if len(all_reviews) <= 3:
                pag = False
                print('ok4')
                print(rev[0], rev[1])
                await bot.delete_message(id_user, message_id=call.message.message_id)
                await bot.send_photo(id_user, rev[0], rev[1],
                                     reply_markup=keyboard.pagination(number=0,
                                                                      len_rew=len(reviews[0]),
                                                                      number_file_read=number_file_read,
                                                                      prew='1',
                                                                      pag=pag))
            else:
                print('ok4')
                print(rev[0], '|', rev[1])
                print(rev)
                await bot.delete_message(id_user, message_id=call.message.message_id)
                await bot.send_photo(id_user, rev[0], rev[1],
                                     reply_markup=keyboard.pagination(number=0,
                                                                      len_rew=len(reviews[0]),
                                                                      number_file_read=number_file_read,
                                                                      prew='1',
                                                                      pag=pag))
            await call.answer()

        except Exception as e:
            print("asdasd", e)
            raise e
            await call.answer('Нет отзывов', )

    elif data[0] == "main_menu":
        await bot.delete_message(id_user, message_id=call.message.message_id)
        await call.message.answer(
            'Выберите и нажмите на кнопку ниже!',
            reply_markup=keyboard.menu_start())
        await call.answer()

    elif data[0] == "ignore":
        await call.answer()

    elif data[0] == "callme_name":
        await bot.delete_message(id_user, message_id=call.message.message_id)
        await call.message.answer(
            'Ответье на 3 вопроса',
            reply_markup=keyboard.call_state())
        await call.message.answer('Как вас зовут?')
        await Form.callme_name.set()
        await call.answer()

    elif data[0] == "callme_number":
        if call.message.chat.type == 'private':
            sent_msg = await call.message.answer('Отлично. Оставьте нам свой телефон, чтобы мы с вами связались', reply_markup=keyboard.number_request())
           # if id_user in msgs_to_del.keys():
            #    msgs_to_del[id_user].append(sent_msg.message_id)
           # else:
            #    msgs_to_del[id_user] = []
            await Form.callme_number.set()
            await call.answer()

    elif data[0] == "callme_subject":
            await call.message.answer('Спасибо. И последнее: по какому вопросу/теме обращаетесь?')
            await Form.callme_subject.set()
            await call.answer()

    elif data[0] == "callme":
        await bot.delete_message(id_user, message_id=call.message.message_id)
        await call.message.answer(
            'Оставьте ваши контактные данные в следующем формате:\n'
            '\n'
            'Имя: Alex\n'
            'Телефон: +351987987987\n'
            'Тема: Хочу купить курс "Crypto Camp"\n',
            reply_markup=keyboard.call_state())
        if call.message.chat.type == 'private':
            sent_msg = await call.message.answer("Поделитесь своим номером", reply_markup=keyboard.number_request())
            if id_user in msgs_to_del.keys():
                msgs_to_del[id_user].append(sent_msg.message_id)
            else:
                msgs_to_del[id_user] = []

        await Form.callme.set()
        await call.answer()

    elif data[0] == "sendtogroup":
        await bot.delete_message(id_user, message_id=call.message.message_id)
        await call.message.answer(
            'Спасибо мы приняли вашу заявку, ожидайте звонок от нас',
            reply_markup=keyboard.main())
#        for msg in msgs_to_del[id_user]:
#            await bot.delete_message(id_user, message_id=msg)
#        msgs_to_del[id_user] = []

        user_message = call.message.reply_to_message.text
        user = call.message.reply_to_message['from']

        async with state.proxy() as data:
            print(data)
            # await bot.send_message(-1001624336092, "{} \n\nзаявку отправил:\nUserId: {}\nName: {}\nUserName: @{}".format(user_message, user.id, user['first_name'], user['username']))

            await user_methods.send_message(id=user.id, text=("{} \n\nзаявку отправил:\nUserId: {}\nName: {}\nUserName: @{}".format(data['text'], user.id, user['first_name'], user['username'])),
                                        nickname=user['first_name'], is_call=True, contact=data['contact'], name=data['name'])
        await state.finish()

    elif data[0] == "feedback":
        if str(id_user) not in users_in_chat.keys():
            users_in_chat[str(id_user)] = True
        await bot.edit_message_text('Напишите ваш вопрос и мы ответим вам в ближайшее время.\nОбычно мы отвечаем в течение дня, но в связи с большим кол-вом заявок ответ может задержаться', call.message.chat.id, call.message.message_id)
        await bot.edit_message_reply_markup(call.message.chat.id,
                                    call.message.message_id,
                                    reply_markup=keyboard.chat_state())
        await Form.feedback.set()
    
    elif data[0] == "stop_chatting":
        try:
            users_in_chat.pop(str(id_user))
        except KeyError:
            pass
        await bot.delete_message(id_user, message_id=call.message.message_id)
        await bot.send_message(id_user, 'Чат прерван. Чтобы опять связаться с нашим менеджером, нажмите кнопку «Написать нам.». ')
        await call.message.answer(
            'Выберите и нажмите на кнопку ниже!',
            reply_markup=keyboard.menu_start())
        await state.finish()
    
    elif data[0] == "stop_call":
        await bot.delete_message(id_user, message_id=call.message.message_id)
        await call.message.answer(
            'Запрос отменен',
            reply_markup=keyboard.menu_back())
        await call.message.answer('Запрос отменен', reply_markup=keyboard.main())
        
#        for msg in msgs_to_del[id_user]:
#            await bot.delete_message(id_user, message_id=msg)
#        msgs_to_del[id_user] = []
        await state.finish()


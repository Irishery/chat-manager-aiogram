from aiogram import types
from misc import *
import csv
import funk
import keyboard


users = []


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
        number_file_read = data[1]
        try:
            pag = True
            all_reviews = funk.see_rew(number_file_read)
            rev = all_reviews[0]
            reviews = funk.sort_reviews(all_reviews)
            if len(all_reviews) <= 3:
                pag = False
                await bot.delete_message(id_user, message_id=call.message.message_id)
                await bot.send_photo(id_user, rev[0], rev[1],
                                     reply_markup=keyboard.pagination(number=0,
                                                                      len_rew=len(reviews[0]),
                                                                      number_file_read=number_file_read,
                                                                      prew='1',
                                                                      pag=pag))
            else:
                await bot.delete_message(id_user, message_id=call.message.message_id)
                await bot.send_photo(id_user, rev[0], rev[1],
                                     reply_markup=keyboard.pagination(number=0,
                                                                      len_rew=len(reviews[0]),
                                                                      number_file_read=number_file_read,
                                                                      prew='1',
                                                                      pag=pag))
            await call.answer()

        except:
            await call.answer('Нет отзывов', )

    elif data[0] == "main_menu":
        await bot.delete_message(id_user, message_id=call.message.message_id)
        await call.message.answer(
            'Выберите и нажмите на кнопку ниже!',
            reply_markup=keyboard.menu_start())
        await call.answer()

    elif data[0] == "ignore":
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
        await Form.callme.set()
        await call.answer()

    elif data[0] == "sendtogroup":
        await bot.delete_message(id_user, message_id=call.message.message_id)
        await call.message.answer(
            'Спасибо мы приняли вашу заявку, ожидайте звонок от нас',
            reply_markup=keyboard.menu_back())
        async with state.proxy() as data:
            await bot.send_message(-1001624336092, "{} \n\nзаявку отправил:\nUserId: {}\nName: {}\nUserName: @{}".format(data['text'], id_user, data['fname'], data['uname']))
        await state.finish()

    elif data[0] == "feedback":
        await bot.edit_message_reply_markup(call.message.chat.id,
                                    call.message.message_id,
                                    reply_markup=keyboard.chat_state())
        await Form.feedback.set()
    
    elif data[0] == "stop_chatting":
        await bot.delete_message(id_user, message_id=call.message.message_id)
        await call.message.answer(
            'Чат закрыт',
            reply_markup=keyboard.menu_back())
        await state.finish()
    
    elif data[0] == "stop_call":
        await bot.delete_message(id_user, message_id=call.message.message_id)
        await call.message.answer(
            'Запрос отменен',
            reply_markup=keyboard.menu_back())
        await state.finish()


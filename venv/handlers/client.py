from json import load

from aiogram import types, Dispatcher
from create_bot import bot
from database import basket, LMS
from database.main_database_coach_ticket import Coach, SeasonTicket
from markup import markup, admin_markup
from datetime import datetime, timedelta
import locale

locale.setlocale(locale.LC_ALL, "")

database_mongo = basket.WorkMongo(27017, 'tg_bot', 'basket')

user_cab = LMS.LMS(27017, 'tg_bot', 'LMS')


# open file for admin id
with open(r'D:\telegram_shop\venv\admin.json') as read_json:
    admin_dict = load(read_json)


def find_price(find_price: str):
    '''
    this function find price in message
    :param find_price:
    :return price
    '''
    find_price = find_price.replace('\n', ' ').split(' ')
    for el in find_price:

        if el.isdigit():
            return el


async def send_welcome(message: types.Message):
    '''
    greeting with bot and reply markup
    :param message:
    '''
    if user_cab.cheak_user_on_LMS(f'{message.from_user.id}'):

        await message.reply(f'Привіт {message.from_user.username}, вітаємо у нашому спорт клубі)',
                            reply_markup=markup.add_but)
    else:
        # add user in database LMS
        user_cab.add_user({
            '_id': f'{message.from_user.id}',
            'first_name': message.from_user.first_name,
            'active_object': [],
            'history': []
        })

        await message.reply(
            f'Привіт {message.from_user.username}, вітаємо у нашому спорт клубі), бачу ти новенький, ми тебе добавили в базу',
            reply_markup=markup.add_but)


async def get_admin(message: types.Message):
    '''
    open Admin mode
    :param message:
    '''
    if message.from_user.id in admin_dict['admin']:
        await message.answer('Hi Admin', reply_markup=admin_markup.add_coach_ticket)


async def get_answer(message: types.Message):
    '''
    get answer on text button
    :param message:
    '''
    if message.text == 'Тренер':
        for coach in Coach.select():
            await message.answer_photo(photo=coach.picture,
                                       caption=f'Звуть - {coach.name}\nЦіна - {coach.price}\n\n{coach.description}\n\nid - {coach.id}',
                                       reply_markup=markup.basket_button_add)


    elif message.text == 'Корзина':

        if database_mongo.search_user(f'{message.from_user.id}'):
            for item in database_mongo.cheak_user(f'{message.from_user.id}'):

                if not 'photo' in item.keys():

                    await message.answer(f'{item["text"]}', reply_markup=markup.remove_and_back)

                elif not 'text' in item.keys():

                    await message.answer_photo(photo=item['photo'], caption=f'{item["caption"]}',
                                               reply_markup=markup.remove_and_back)

            else:
                await message.answer('Що далі ?', reply_markup=markup.pay_button)
        else:
            await message.answer('ваша корзина пуста', reply_markup=markup.empty_basket_back)

    elif message.text == 'Абонимент':

        await message.answer('Обери хто ти ', reply_markup=markup.inline_add)

    elif message.text == 'Графік роботи':
        await message.answer("Понеділок - П'ятниця 10:00 - 20:00\nСубота 10:00 - 18:00\nНеділя 10:00 - 18:00",
                             reply_markup=markup.back_main_menu_add)


# @dp.callback_query_handler(lambda call: True)
async def get_qeary(call: types.CallbackQuery):
    '''
    answer to inline button
    :param call:
    '''

    # Абонимент -> Студент
    if call.data == 'student_1':
        for el in SeasonTicket.select():

            # this algorithm searches for a student card

            if el.type == 'Студенський':
                await call.message.answer(
                    f'Тип абонимента - {el.type}\nТип тренувань - {el.type_train}\nЦіна - {el.price}\n\nid - {el.id}',
                    reply_markup=markup.basket_button_add)

    # Абонимент -> Дорослий
    elif call.data == 'adult_1':

        for adult in SeasonTicket.select():

            if adult.type == 'Дорослий':
                await call.message.answer(f'Тип абонимента - {adult.type}\nТип тренувань - {adult.type_train}\nЦіна - {adult.price}\n\nid - {adult.id}',
                                       reply_markup=markup.basket_button_add)

    elif call.data == 'return_back':
        await call.message.answer('повертаюсь..', reply_markup=markup.add_but)

    elif call.data == 'return_back_from_product':
        await call.message.answer('повертаюсь..', reply_markup=markup.add_but)

    # answer for add to basket
    elif call.data == 'add_to_basket':

        if not call.message.photo:
            # add to basket(MongoDB) ticket
            database_mongo.add_to_basket({'id_user': f'{call.from_user.id}',
                                          'text': f'{call.message.text}',
                                          'price': f'{find_price(call.message.text)}'
                                          })

            await call.message.answer('успішно збереженно', reply_markup=markup.add_but)


        elif call.message.photo:

            # add to basket(MongoDB) coach
            database_mongo.add_to_basket({
                'id_user': f'{call.from_user.id}',
                'photo': call.message.photo[0].file_id,
                'caption': f'{call.message.caption}',
                'price': f'{find_price(call.message.caption)}'

            })

            await call.message.answer('успішно збереженно', reply_markup=markup.add_but)

    # for remove from basket
    elif call.data == 'remove_from_basket':
        if call.message.photo:

            database_mongo.delete_from_basket(id_user=call.from_user.id, caption=call.message.caption)

        elif not call.message.photo:

            database_mongo.delete_from_basket(id_user=call.from_user.id, text=call.message.text)

    elif call.data == 'pay_product':
        now = datetime.now()
        next_month = now + timedelta(days=30)

        for basket in database_mongo.cheak_user(f'{call.from_user.id}'):
            keyss = basket.keys()

            try:

                if 'photo' in keyss:

                    user_cab.add_data(f'{call.from_user.id}', f'{call.from_user.first_name}', {
                        'photo': basket['photo'],
                        'caption': basket['caption'],
                        'price': basket['price']
                    })

                elif 'text' in keyss:

                    user_cab.add_data(
                        f'{call.from_user.id}', f'{call.from_user.first_name}',
                        {
                            'text': basket['text'],
                            'price': basket['price'],
                        }
                    )

                    user_cab.add_data(
                        f'{call.from_user.id}', f'{call.from_user.first_name}',
                        {
                            'text': basket['text'],
                            'price': basket['price'],
                            'start_time': now.strftime('%d %B %Y'),
                            'finish_time': next_month.strftime('%d %B %Y')
                        }, where='active_object'
                    )

            except KeyError:
                pass

        await call.message.answer(f'Вартість покупки - {database_mongo.count_price(call.from_user.id)}')

        database_mongo.clear_basket(f'{call.from_user.id}')

    elif call.data == 'delete_coach_admin':

        Coach.delete_by_id(call.message.caption.split(' ')[-1])

        await call.message.reply('Успішно видаленно\nЩо далі ?', reply_markup=admin_markup.admin_button)

    elif call.data == 'delete_ticket_admin':

        SeasonTicket.delete_by_id(call.message.text.split(' ')[-1])

        await call.message.reply('Успішно видаленно\nЩо далі ?', reply_markup=admin_markup.admin_button)


def register_handlers_client(dp: Dispatcher):
    '''
    register handler
    :param dp
    '''# @dp.callback_query_handler(lambda call: True)
    # dp.register_message_handler(open_LMS, commands=['LMS'])
    dp.register_message_handler(get_admin, commands=['Додати'])
    dp.register_message_handler(send_welcome, commands=['start'])
    dp.register_message_handler(get_answer)
    dp.register_callback_query_handler(get_qeary)
# @dp.callback_query_handler(lambda call: True)
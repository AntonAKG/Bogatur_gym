from json import load

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from create_bot import dp
from database.main_database_coach_ticket import Coach
from markup import admin_markup

# open json file with id admin
with open(r'D:\telegram_shop\venv\admin.json') as read_json:
    admin_dict = load(read_json)


class FSM_admin_coach(StatesGroup):
    '''
    class for FSM storage and state
    '''
    photo = State()
    name = State()
    description = State()
    price = State()


@dp.message_handler(commands='Створити_тренера', state=None)
async def cm_start(message: types.Message):
    '''
    this function start FSM mode
    :param message:
    '''
    if message.from_user.id in admin_dict['admin']:
        await FSM_admin_coach.photo.set()
        await message.reply('Загрузіть фото')


@dp.message_handler(content_types=['photo'], state=FSM_admin_coach.photo)
async def load_photo(message: types.Message, state: FSMContext):
    '''
    this function catch photo and save
    :param message:
    :param state:
    '''
    if message.from_user.id in admin_dict['admin']:
        async with state.proxy() as data:
            data['photo'] = message.photo[0].file_id
        await FSM_admin_coach.next()
        await message.reply('Введи імя')


@dp.message_handler(state=FSM_admin_coach.name)
async def load_name(message: types.Message, state: FSMContext):
    '''
    this function catch coach name and save
    :param message:
    :param state:
    '''
    if message.from_user.id in admin_dict['admin']:
        async with state.proxy() as data:
            data['name'] = message.text

        await FSM_admin_coach.next()
        await message.reply('Введи опис')


@dp.message_handler(state=FSM_admin_coach.description)
async def load_description(message: types.Message, state: FSMContext):
    '''
    this function catch description and save it
    :param message:
    :param state:
    '''
    if message.from_user.id in admin_dict['admin']:
        async with state.proxy() as data:
            data['description'] = message.text

        await FSM_admin_coach.next()
        await message.reply('Введи ціну')


@dp.message_handler(state=FSM_admin_coach.price)
async def load_price(message: types.Message, state: FSMContext):
    '''
    this function catch price and write data on database
    :param message:
    :param state:
    '''
    if message.from_user.id in admin_dict['admin']:
        async with state.proxy() as data:
            data['price'] = float(message.text)

        async with state.proxy() as data:

            ob_1 = Coach(name=data['name'], description=data['description'], price=data['price'],
                                picture=data["photo"])
            ob_1.save()
            await message.reply('Дані успішно збереження', reply_markup=admin_markup.admin_button)

        await state.finish()


@dp.message_handler(state="*", commands='stop')
@dp.message_handler(Text(equals='stop', ignore_case=True), state="*")
async def cancel_handler(message: types.Message, state: FSMContext):
    '''
    this function for leave from FSM mode
    :param message:
    :param state:
    '''
    if message.from_user.id in admin_dict['admin']:
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.finish()
        await message.answer('Вихожу...', reply_markup=admin_markup.admin_button)
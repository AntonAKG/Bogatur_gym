from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from create_bot import dp
from json import load
from markup import admin_markup
from database.main_database_coach_ticket import SeasonTicket

with open(r'D:\telegram_shop\venv\admin.json') as read_json:
    admin_dict = load(read_json)


class FSM_admin_ticket(StatesGroup):
    '''
    class for fsm storage
    '''
    type = State()
    type_train = State()
    price = State()

@dp.message_handler(commands='Створити_абонимент', state=None)
async def cm_start(message:types.Message):
    '''
    function start FSM
    :param message:
    '''
    if message.from_user.id in admin_dict['admin']:
        await FSM_admin_ticket.type.set()
        await message.reply('введіть тип абонимента (Студентський - Дорослий)', reply_markup=admin_markup.add_student_adult)

@dp.message_handler(state=FSM_admin_ticket.type)
async def load_type(message: types.Message, state : FSMContext):
    '''
    catch type student or adult
    :param message:
    :param state:
    '''
    if message.from_user.id in admin_dict['admin']:
        async with state.proxy() as data:
            data['type'] = message.text
        await FSM_admin_ticket.next()
        await message.reply('Введіть тип тренування', reply_markup=admin_markup.add_one_student_button if data['type'] == 'Студенський' else admin_markup.add_full_semi)

@dp.message_handler(state=FSM_admin_ticket.type_train)
async def load_type_train(message:types.Message, state: FSMContext):
    '''
    catch type_train full morning or evening
    :param message:
    :param state:
    '''
    if message.from_user.id in admin_dict['admin']:
        async with state.proxy() as data:
            data['type_train'] = message.text

        await FSM_admin_ticket.next()
        await message.reply('Введіть ціну')

@dp.message_handler(state=FSM_admin_ticket.price)
async def load_price(message:types.Message, state: FSMContext):
    '''
    catch price, and write data on database
    :param message:
    :param state:
    '''
    if message.from_user.id in admin_dict['admin']:
        async with state.proxy() as data:
            data['price'] = int(message.text)

        async with state.proxy() as data:

            save_data = SeasonTicket(type = data['type'], type_train = data['type_train'], price = int(data['price']))
            save_data.save()
            await message.reply("Дані успішно збереженні", reply_markup=admin_markup.admin_button)

        await state.finish()

@dp.message_handler(state="*", commands='stop')
@dp.message_handler(Text(equals='stop', ignore_case=True), state="*")
async def cancel_handler(message: types.Message, state: FSMContext):
    '''
    function for leave from FSM mode
    :param message:
    :param state:
    '''
    if message.from_user.id in admin_dict['admin']:
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.finish()
        await message.answer('Вихожу...', reply_markup=admin_markup.admin_button)
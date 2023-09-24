from json import load

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from create_bot import dp
from database.main_database_coach_ticket import SeasonTicket, Coach
from markup import admin_markup

with open(r'D:\telegram_shop\venv\admin.json') as read_json:
    admin_dict = load(read_json)


class FSM_delete(StatesGroup):
    '''
    start FSM delete
    '''
    action = State()


@dp.message_handler(commands='Видалити', state=None)
async def delete_ticket(message: types.Message):
    '''
    work with commands delete
    :param message:
    '''
    if message.from_user.id in admin_dict['admin']:
        await FSM_delete.action.set()
        await message.reply('Оберіть що будете видаляти', reply_markup=admin_markup.add_delete)


@dp.message_handler(state=FSM_delete.action)
async def get_action(message: types.Message, state: FSMContext):
    '''
    choose what we will delete
    :param message:
    :param state:
    '''
    if message.from_user.id in admin_dict['admin']:
        if message.text == 'Тренера':
            for coach in Coach.select():
                await message.reply_photo(photo=coach.picture,
                                          caption=f'Звуть - {coach.name}\nЦіна - {coach.price}\n\n{coach.description}\n\nid товару - {coach.id}',
                                          reply_markup=admin_markup.inline_add_coach)

        elif message.text == 'Абонимента':

            for ticket in SeasonTicket.select():
                await message.reply(
                    f'Тип абонимента - {ticket.type}\nТип тренувань - {ticket.type_train}\nЦіна - {ticket.price}\n\nid товару - {ticket.id}',
                    reply_markup=admin_markup.inline_add_ticket)

        await state.finish()


@dp.message_handler(state="*", commands='stop')
@dp.message_handler(Text(equals='stop', ignore_case=True), state="*")
async def cancel_handler(message: types.Message, state: FSMContext):
    '''
    function for stop FSM mode
    :param message:
    :param state:
    '''
    if message.from_user.id in admin_dict['admin']:
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.finish()
        await message.answer('Вихожу...', reply_markup=markup.add_but)
import locale
from datetime import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from create_bot import dp
from handlers.client import user_cab
from markup import markup
from aiogram.dispatcher.filters import Text

# Ukraine local
locale.setlocale(locale.LC_ALL, "")
now = datetime.now()


class LMS_state(StatesGroup):
    '''
    class for FSM
    '''
    action = State()


@dp.message_handler(commands='LMS', state=None)
async def open_LMS(message: types.Message):
    '''
    start FSM
    :param message:
    '''
    await LMS_state.action.set()
    await message.reply('Що будемо робити ?', reply_markup=markup.LMS_add)


@dp.message_handler(state=LMS_state.action)
async def get_action(message: types.Message, state: FSMContext):
    '''
    function for work history and active ticket
    :param message:
    '''
    if message.text == 'Історія замовлень':
        # cheak user in database
        if user_cab.cheak_user_on_LMS(f'{message.from_user.id}'):

            # get info about his history
            for data in user_cab.get_info(f'{message.from_user.id}', f'{message.from_user.first_name}'):
                if data['history']:

                    for dicts in data['history']:
                        keyy = dicts.keys()

                        try:

                            if 'text' in keyy:

                                await message.answer(f"{dicts['text']}\n{dicts['time']}", reply_markup=markup.add_but)

                            elif 'photo' in keyy:
                                await message.answer_photo(photo=dicts['photo'],
                                                           caption=f"{dicts['caption']}", reply_markup=markup.add_but)


                        except KeyError:
                            pass
                else:
                    await message.answer('Ваша історія пуста', reply_markup=markup.add_but)


    # answer active ticket
    elif message.text == 'Активні абонименти':
        if user_cab.cheak_user_on_LMS(f'{message.from_user.id}'):
            for data in user_cab.get_info(f'{message.from_user.id}', f'{message.from_user.first_name}'):
                # cheak ticket in database
                if data['active_object']:

                    for dicts in data['active_object']:

                        # cheak deadline ticket
                        if now.strftime('%d %B %Y') > dicts['finish_time']:
                            await message.answer('У вас немає активного абонименту')

                        else:
                            await message.answer(
                                f'{dicts["text"]}\nАктивний з {dicts["start_time"]}\nПо {dicts["finish_time"]}')
                else:
                    await message.answer('У вас немає активного абонименту')
    await state.finish()

@dp.message_handler(state="*", commands='Вийти')
@dp.message_handler(Text(equals='Вийти', ignore_case=True), state="*")
async def cancel_handler(message: types.Message, state: FSMContext):
    '''
    function for stop FSM mode
    :param message:
    :param state:
    '''

    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.answer('Вихожу...', reply_markup=markup.add_but)





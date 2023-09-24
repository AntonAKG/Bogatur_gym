import logging

from aiogram import executor
from create_bot import dp

logging.basicConfig(level=logging.INFO)



async def on_startup(_):
    '''
    this function reports where bot start
    :param _:
    '''
    print('бот вийшов в онлайн')

from handlers import client

client.register_handlers_client(dp)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)

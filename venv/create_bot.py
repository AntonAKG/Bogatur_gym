from aiogram import Bot ,Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()

# create bot
bot = Bot(token='6229948082:AAEKLgNe6tIkyrJRGn-H0KzDtXlZDYVKCl4')
dp = Dispatcher(bot, storage=storage)
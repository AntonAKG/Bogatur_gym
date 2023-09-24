from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

# admin menu first step on admin mode

coach = KeyboardButton('/Створити_тренера')
ticket = KeyboardButton('/Створити_абонимент')

add_coach_ticket = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(coach, ticket)

# choose a type ticket (admin mode) student/adult

student = KeyboardButton('Студенський')
adult = KeyboardButton('Дорослий')

add_student_adult = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(student, adult)

# choose type train

full_day = KeyboardButton('Повний')
evening = KeyboardButton('Вечірній')
morning = KeyboardButton('Денний')

add_full_semi = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(full_day,evening, morning)

# button for delete

del_ticket = KeyboardButton('Абонимента')
del_coach = KeyboardButton('Тренера')

add_delete = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(del_coach, del_ticket)

# button for choose student full day

one_student_button = KeyboardButton('Повний')
add_one_student_button = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(one_student_button)
# inline button for coach delete

remove_product = InlineKeyboardButton('Видалити', callback_data='delete_coach_admin')
inline_add_coach = InlineKeyboardMarkup().add(remove_product)

# inline button for ticket delete

ticket_remove = InlineKeyboardButton('Видалити', callback_data='delete_ticket_admin')
inline_add_ticket = InlineKeyboardMarkup().add(ticket_remove)

# button after remove admin

return_start = KeyboardButton('/start')
return_admin = KeyboardButton('/Додати')
return_delete = KeyboardButton('/Видалити')

admin_button = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(return_start, return_admin,return_delete)

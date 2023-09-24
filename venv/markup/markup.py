from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup


# main menu
menu_button_1 = KeyboardButton('Тренер')
menu_button_2 = KeyboardButton('Корзина')
menu_button_3 = KeyboardButton('Абонимент')
menu_button_4 = KeyboardButton('Графік роботи')

add_but = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(menu_button_1,menu_button_2,menu_button_3,menu_button_4)

# inline button for season ticket

inline_button_1 = InlineKeyboardButton('Студент', callback_data='student_1')
inline_button_2 = InlineKeyboardButton('Дорослий' ,callback_data='adult_1')
inline_add = InlineKeyboardMarkup().add(inline_button_1, inline_button_2)

# button for return to main menu

back_main_menu = InlineKeyboardButton('Повернутись назад', callback_data='return_back')
back_main_menu_add = InlineKeyboardMarkup().add(back_main_menu)

# button for add in basket and return to main menu from product

basket_button = InlineKeyboardButton('Додати до корзини', callback_data='add_to_basket')
basket_button_back_in_main = InlineKeyboardButton('Повернутись назад', callback_data='return_back_from_product')
basket_button_add = InlineKeyboardMarkup().add(basket_button, basket_button_back_in_main)

# remove from basket and retunr back

remove = InlineKeyboardButton('Видалити з корзини', callback_data='remove_from_basket')
menu_remove = InlineKeyboardButton('Повернутись назад', callback_data="return_back_from_product")
remove_and_back = InlineKeyboardMarkup().add(remove, menu_remove)

# button for pay

pay_but = InlineKeyboardButton('Оплатити', callback_data='pay_product')
pay_back = InlineKeyboardButton('Повернутись назад' , callback_data='return_back_from_product')
pay_button = InlineKeyboardMarkup().add(pay_but, pay_back)

# from empty basket return back

empty_back = InlineKeyboardButton('Повернутись назад', callback_data='return_back_from_product')
empty_basket_back = InlineKeyboardMarkup().add(empty_back)

# for LMS

LMS_menu = KeyboardButton('Історія замовлень')
LMS_active = KeyboardButton('Активні абонименти')
LMS_leave = KeyboardButton("/Вийти")

LMS_add = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(LMS_menu, LMS_active, LMS_leave)
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


keyboard_1 = KeyboardButton('/start')
keyboard_2 = KeyboardButton('/status_item')
keyboard_3 = KeyboardButton('/on_market')


buttons = ReplyKeyboardMarkup(resize_keyboard=True).row(keyboard_1, keyboard_2, keyboard_3)

# start_keyboard = KeyboardButton('/start')
# buttons_start = ReplyKeyboardMarkup(resize_keyboard=True)
# buttons_start.add(start_keyboard)
#
#
# on_market_keyboard = KeyboardButton('/on_market')
# buttons_market = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
# buttons_market.add(on_market_keyboard)

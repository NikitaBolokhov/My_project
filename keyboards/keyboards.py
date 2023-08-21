from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from lexicon.lexicon_ru import LEXICON_RU

button_game: KeyboardButton = KeyboardButton(
                  text=LEXICON_RU['name_button_game'])
button_stat: KeyboardButton = KeyboardButton(
                  text=LEXICON_RU['name_button_stat'])
button_exit: KeyboardButton = KeyboardButton(
                  text=LEXICON_RU['name_button_exit'])

game_kb_builder: ReplyKeyboardBuilder = ReplyKeyboardBuilder()
game_kb_builder.row(button_game, button_stat, button_exit)
game_kb: ReplyKeyboardMarkup = game_kb_builder.as_markup(
                                    one_time_keyboard=True,
                                    resize_keyboard=True)

stat_kb_builder: ReplyKeyboardBuilder = ReplyKeyboardBuilder()
stat_kb_builder.row(button_game, button_exit)
stat_kb: ReplyKeyboardMarkup = stat_kb_builder.as_markup(
                                     one_time_keyboard=True,
                                     resize_keyboard=True)

exit_kb_builder: ReplyKeyboardBuilder = ReplyKeyboardBuilder()
exit_kb_builder.row(button_exit)
exit_kb: ReplyKeyboardMarkup = exit_kb_builder.as_markup(
                                     one_time_keyboard=True,
                                     resize_keyboard=True)

from aiogram.types import (KeyboardButton, ReplyKeyboardMarkup,
                           InlineKeyboardButton, InlineKeyboardMarkup)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


# Функция-генератор, возвращающая обычную клавиатуру
def regular_keyboard(buttons: list,
                     width: int = 3,
                     one_time_keyboard: bool = True,
                     resize_keyboard: bool = True) -> ReplyKeyboardMarkup:
    res: list[KeyboardButton] = [KeyboardButton(text=but) for but in buttons]
    kb_builder: ReplyKeyboardBuilder = ReplyKeyboardBuilder()
    kb_builder.row(*res, width=width)
    kb: ReplyKeyboardMarkup = kb_builder.as_markup(
                                    one_time_keyboard=one_time_keyboard,
                                    resize_keyboard=resize_keyboard)
    return kb


# Функция-генератор, возвращающая инлайн клавиатуру
def inline_keyboard(buttons: dict[str: str],
                    width: int = 3) -> InlineKeyboardMarkup:
    res: list[InlineKeyboardButton] = [InlineKeyboardButton(
                                        text=key,
                                        callback_data=value
                                        ) for key, value in buttons.items()]
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    kb_builder.row(*res, width=width)
    kb: InlineKeyboardMarkup = kb_builder.as_markup()
    return kb

import random
import requests

from lexicon.lexicon_ru import LEXICON_RU


# Исходники для игры
ATTEMPTS: int = 6

# Словарь, в котором будут храниться данные пользователя
users: dict = {}


# Функция возвращающая случайное целое число от 1 до 100
def get_random_number() -> int:
    return random.randint(1, 100)


# Функция возвращающая оставшееся количество попыток
def show_attempts(attempt: int) -> str:
    if attempt > 1:
        return f'Доступное количество попыток: <b>{attempt}</b>.'
    elif attempt == 1:
        return '<b>У тебя осталась последняя попытка</b>🤞'
    else:
        return '<b>К сожалению, попыток больше не осталось</b>😿'


# Функция возвращающая случайную картинку с котиком
def get_random_cat() -> tuple[bool, str]:
    cat_response = requests.get('https://api.thecatapi.com/v1/images/search')
    if cat_response.status_code == 200:
        cat_link = cat_response.json()[0]['url']
        return True, cat_link
    else:
        return False,


# Функция возвращающая случайную гифку
def get_random_gif() -> tuple[bool, str]:
    gif_response = requests.get('https://yesno.wtf/api')
    if gif_response.status_code == 200:
        gif_link = gif_response.json()['image']
        return True, gif_link
    else:
        return False,


# Функция, возвращающая случайный выбор бота в игре
def get_bot_choice() -> str:
    return random.choice(['rock', 'paper', 'scissors'])


# Функция, возвращающая ключ из словаря, по которому
# хранится значение, передаваемое как аргумент - выбор пользователя
def _normalize_user_answer(user_answer: str) -> str:
    for key in LEXICON_RU:
        if LEXICON_RU[key] == user_answer:
            break
    return key


# Функция, определяющая победителя
def get_winner(user_choice: str, bot_choice: str) -> str:
    user_choice = _normalize_user_answer(user_choice)
    rules: dict[str, str] = {'rock': 'scissors',
                             'scissors': 'paper',
                             'paper': 'rock'}
    if user_choice == bot_choice:
        return 'nobody_won'
    elif rules[user_choice] == bot_choice:
        return 'user_won'
    else:
        return 'bot_won'

import random
import requests


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
        return f'Доступное количество попыток: {attempt}'
    elif attempt == 1:
        return 'У тебя осталась последняя попытка'
    else:
        return 'К сожалению, попыток больше не осталось :('


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

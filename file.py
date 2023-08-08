import requests
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message
import random

API_TOKEN: str = '6594894121:AAFMgwvN3saHhWBZKKEDA1SH6m8bmkfa3vU'

# Создаем объекты бота и диспетчера
bot: Bot = Bot(token=API_TOKEN)
dp: Dispatcher = Dispatcher()


# Этот хэндлер будет срабатывать на команду "/start"
@dp.message(Command(commands=["start"]))
async def process_start_command(message: Message):
    await message.answer(f'Привет, {message.chat.first_name}!\n '
                         f'Меня зовут Кото-бот!\n '
                         f'Жми /menu и узнай, что я умею')


# Этот хэндлер будет срабатывать на команду "/menu"
@dp.message(Command(commands=["menu"]))
async def process_help_command(message: Message):
    await message.answer('Обычно я играю в попугая и повторяю за тобой, '
                         'но не всегда:\n '
                         '  нажми /cat и я порадую тебя котик(ом/ами)\n '
                         '  нажми /gif и я кину в тебя гифкой\n '
                         '  нажми /game и я поиграю с тобой')


# Этот хэндлер будет срабатывать на команду "/cat"
@dp.message(Command(commands=["cat"]))
async def process_help_command(message: Message):
    cat_response = requests.get('https://api.thecatapi.com/v1/images/search')
    if cat_response.status_code == 200:
        cat_link = cat_response.json()[0]['url']
        await message.reply_photo(cat_link)
    else:
        await message.reply('Сорян котов не будет '
                            'Попробуй снова немного позже')


# Этот хэндлер будет срабатывать на команду "/gif"
@dp.message(Command(commands=["gif"]))
async def process_help_command(message: Message):
    gif_response = requests.get('https://yesno.wtf/api')
    if gif_response.status_code == 200:
        gif_link = gif_response.json()['image']
        await message.reply_animation(gif_link)
    else:
        await message.reply('Сорян гифок не будет '
                            'Попробуй снова немного позже')


# Исходники для игры
ATTEMPTS: int = 6

# Словарь, в котором будут храниться данные пользователя
users: dict = {}


# Функция возвращающая случайное целое число от 1 до 100
def get_random_number() -> int:
    return random.randint(1, 100)


# Функция возвращающая оставшееся количество попыток
def show_attempts(attempt) -> str:
    if attempt > 1:
        return f'Доступное количество попыток: {attempt}'
    elif attempt == 1:
        return 'У тебя осталась последняя попытка'
    else:
        return 'К сожалению, попыток больше не осталось :('


# Этот хэндлер будет срабатывать на команду "/game"
@dp.message(Command(commands=['game']))
async def process_help_command(message: Message):
    if message.from_user.id not in users:
        users[message.from_user.id] = {'in_game': False,
                                       'secret_number': None,
                                       'attempts': None,
                                       'total_games': 0,
                                       'wins': 0}
    await message.answer(f'Правила игры:\n\nЯ загадываю число от 1 до 100, '
                         f'а тебе нужно его угадать\nУ тебя есть {ATTEMPTS} '
                         f'попыток\n\nДоступные команды: '
                         f'\n/cancel - выйти из игры\n '
                         f'/stat - посмотреть статистику\n '
                         f'Я уже загадал число, давай сыграем?')


# Этот хэндлер будет срабатывать на команду "/stat"
@dp.message(Command(commands=['stat']))
async def process_stat_command(message: Message):
    await message.answer(
                    f'Всего игр сыграно: '
                    f'{users[message.from_user.id]["total_games"]}\n'
                    f'Игр выиграно: {users[message.from_user.id]["wins"]}')


# Этот хэндлер будет срабатывать на команду "/cancel"
@dp.message(Command(commands=['cancel']))
async def process_cancel_command(message: Message):
    if users[message.from_user.id]['in_game']:
        await message.answer('Жаль, что ты уходишь(.\n '
                             'Если захочешь поиграть со мной '
                             'снова - просто дай мне знать')
        users[message.from_user.id]['in_game'] = False
    else:
        await message.answer('А мы итак с тобой не играем. '
                             'Может, сыграем разок?')


# Этот хэндлер будет срабатывать на согласие пользователя сыграть в игру
@dp.message(F.text.lower().in_(['да', 'давай', 'сыграем', 'игра', 'играть', 'хочу играть']))
async def process_positive_answer(message: Message):
    if not users[message.from_user.id]['in_game']:
        await message.answer('Ура!\n\nЯ загадал число от 1 до 100, '
                             'попробуй угадать!')
        users[message.from_user.id]['in_game'] = True
        users[message.from_user.id]['secret_number'] = get_random_number()
        users[message.from_user.id]['attempts'] = ATTEMPTS
    else:
        await message.answer('Пока мы играем в игру я могу '
                             'реагировать только на числа от 1 до 100 '
                             'и команды /cancel и /stat')


# Этот хэндлер будет срабатывать на отказ пользователя сыграть в игру
@dp.message(F.text.lower().in_(['нет', 'не', 'не хочу', 'не буду']))
async def process_negative_answer(message: Message):
    if not users[message.from_user.id]['in_game']:
        await message.answer('Жаль :(\n\nЕсли захочешь поиграть - просто '
                             'дай мне знать')
    else:
        await message.answer('Мы же сейчас с тобой играем. Присылай, '
                             'пожалуйста, числа от 1 до 100')


# Этот хэндлер будет срабатывать на отправку пользователем чисел от 1 до 100
@dp.message(lambda x: x.text and x.text.isdigit() and 1 <= int(x.text) <= 100)
async def process_numbers_answer(message: Message):
    if users[message.from_user.id]['in_game']:
        if int(message.text) == users[message.from_user.id]['secret_number']:
            await message.answer('Ура!!! Ты угадал(а) число!\n\n '
                                 'Ты просто СУПЕР!!!\n '
                                 'Давай, сыграем еще раз?\n '
                                 'Или нажми /stat, если хочешь посмотреть статистику игр')
            users[message.from_user.id]['in_game'] = False
            users[message.from_user.id]['total_games'] += 1
            users[message.from_user.id]['wins'] += 1
        elif int(message.text) > users[message.from_user.id]['secret_number']:
            users[message.from_user.id]['attempts'] -= 1
            await message.answer('Мое число меньше')
            await message.answer(show_attempts(users[message.from_user.id]['attempts']))
        elif int(message.text) < users[message.from_user.id]['secret_number']:
            users[message.from_user.id]['attempts'] -= 1
            await message.answer('Мое число больше')
            await message.answer(show_attempts(users[message.from_user.id]['attempts']))

        if users[message.from_user.id]['attempts'] == 0:
            await message.answer(
                    f'Ты проиграл(а) :(\n\nМое число '
                    f'было {users[message.from_user.id]["secret_number"]} '
                    f'\n Жми /stat, если хочешь посмотреть статистику игр '
                    f'\n\nИли давай сыграем еще раз?')
            users[message.from_user.id]['in_game'] = False
            users[message.from_user.id]['total_games'] += 1
    else:
        await message.answer('Мы еще не играем. Хочешь поиграть?')


# Этот хэндлер будет срабатывать на остальные текстовые сообщения
@dp.message()
async def process_other_text_answers(message: Message):
    if users[message.from_user.id]['in_game']:
        await message.answer('Мы же сейчас играем. '
                             'Присылай, пожалуйста, только числа от 1 до 100')
    else:
        try:
            await message.copy_to(chat_id=message.chat.id)
        except TypeError:
            await message.reply(text='Данный тип апдейтов не поддерживается '
                                     'методом send_copy')


if __name__ == '__main__':
    dp.run_polling(bot)

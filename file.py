import requests
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message
import random
from environs import Env

# Получение доступа к файлу ".env" со скрытыми данными
env = Env()
env.read_env()

bot_token: str = env('BOT_TOKEN')

# Создаем объекты бота и диспетчера
bot: Bot = Bot(token=bot_token)
dp: Dispatcher = Dispatcher()


# Этот хэндлер будет срабатывать на команду "/start"
@dp.message(Command(commands=["start"]))
async def process_start_command(message: Message):
    if message.from_user.id in users and users[message.from_user.id]['in_game']:
        await message.answer('Мы же сейчас играем. '
                             'Присылай, пожалуйста, только числа от 1 до 100 '
                             'или нажми /cancel, если не хочешь продолжать игру')
    else:
        await message.answer(f'Привет, {message.chat.first_name}!\n '
                             f'Меня зовут Кото-бот!\n '
                             f'Жми /menu и узнай, что я умею')


# Этот хэндлер будет срабатывать на команду "/menu"
@dp.message(Command(commands=["menu"]))
async def process_menu_command(message: Message):
    if message.from_user.id in users and users[message.from_user.id]['in_game']:
        await message.answer('Мы же сейчас играем. '
                             'Присылай, пожалуйста, только числа от 1 до 100 '
                             'или нажми /cancel, если не хочешь продолжать игру')
    else:
        await message.answer('Обычно я играю в попугая и повторяю за тобой, '
                             'но не всегда:\n '
                             '  нажми /cat и я порадую тебя котик(ом/ами)\n '
                             '  нажми /gif и я кину в тебя гифкой\n '
                             '  нажми /game и я поиграю с тобой')


# Этот хэндлер будет срабатывать на команду "/cat"
@dp.message(Command(commands=["cat"]))
async def process_cat_command(message: Message):
    if message.from_user.id in users and users[message.from_user.id]['in_game']:
        await message.answer('Мы же сейчас играем. '
                             'Присылай, пожалуйста, только числа от 1 до 100 '
                             'или нажми /cancel, если не хочешь продолжать игру')
    else:
        cat_response = requests.get('https://api.thecatapi.com/v1/images/search')
        if cat_response.status_code == 200:
            cat_link = cat_response.json()[0]['url']
            await message.reply_photo(cat_link)
        else:
            await message.reply('Сорян котов не будет '
                                'Попробуй снова немного позже')


# Этот хэндлер будет срабатывать на команду "/gif"
@dp.message(Command(commands=["gif"]))
async def process_gif_command(message: Message):
    if message.from_user.id in users and users[message.from_user.id]['in_game']:
        await message.answer('Мы же сейчас играем. '
                             'Присылай, пожалуйста, только числа от 1 до 100 '
                             'или нажми /cancel, если не хочешь продолжать игру')
    else:
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
async def process_game_command(message: Message):
    if message.from_user.id not in users:
        users[message.from_user.id] = {'in_game': False,
                                       'secret_number': None,
                                       'attempts': None,
                                       'total_games': 0,
                                       'wins': 0}
    await message.answer(f'Правила игры:\n\nЯ загадываю число от 1 до 100, '
                         f'а тебе нужно его угадать\nУ тебя есть {ATTEMPTS} '
                         f'попыток\n\nДоступные команды:\n '
                         f'/go - начать игру\n '
                         f'/stat - посмотреть статистику\n '
                         f'/cancel - выйти из игры')


# Этот хэндлер будет срабатывать на команду "/stat"
@dp.message(Command(commands=['stat']))
async def process_stat_command(message: Message):
    await message.answer(
                    f'Всего игр сыграно: '
                    f'{users[message.from_user.id]["total_games"]}\n'
                    f'Игр выиграно: {users[message.from_user.id]["wins"]}\n '
                    f'Хочешь поиграть? Жми /game')


# Этот хэндлер будет срабатывать на команду "/cancel"
@dp.message(Command(commands=['cancel']))
async def process_cancel_command(message: Message):
    await message.answer('Жаль, что ты уходишь(.\n '
                         'Если захочешь поиграть со мной '
                         'снова - просто нажми /game')
    users[message.from_user.id]['in_game'] = False


# Этот хэндлер будет срабатывать на команду "/go"
@dp.message(Command(commands=['go']))
async def process_go_command(message: Message):
    if not users[message.from_user.id]['in_game']:
        await message.answer('Ура!\n\nЯ загадал число от 1 до 100, '
                             'попробуй угадать!')
        users[message.from_user.id]['in_game'] = True
        users[message.from_user.id]['secret_number'] = get_random_number()
        users[message.from_user.id]['attempts'] = ATTEMPTS
    else:
        await message.answer('Мы же и так с тобой играем! '
                             'пришли пожалуйста число от 1 до 100')


# Этот хэндлер будет срабатывать на отправку пользователем чисел от 1 до 100
@dp.message(lambda x: x.text and x.text.isdigit() and 1 <= int(x.text) <= 100)
async def process_numbers_answer(message: Message):
    if users[message.from_user.id]['in_game']:
        if int(message.text) == users[message.from_user.id]['secret_number']:
            await message.answer('Ура!!! Ты угадал(а) число!\n\n '
                                 'Ты просто СУПЕР!!!\n '
                                 '\n Жми /stat, если хочешь посмотреть статистику игр '
                                 '\n Жми /go и мы сыграем еще раз')
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
                    f'\n Жми /go и мы сыграем еще раз')
            users[message.from_user.id]['in_game'] = False
            users[message.from_user.id]['total_games'] += 1


# Этот хэндлер будет срабатывать на остальные текстовые сообщения
@dp.message()
async def process_other_text_answers(message: Message):
    if message.from_user.id in users and users[message.from_user.id]['in_game']:
        await message.answer('Мы же сейчас играем. '
                             'Присылай, пожалуйста, только числа от 1 до 100 '
                             'или нажми /cancel, если не хочешь продолжать игру')
    else:
        try:
            await message.copy_to(chat_id=message.chat.id)
        except TypeError:
            await message.reply(text='Данный тип апдейтов не поддерживается '
                                     'методом send_copy')


if __name__ == '__main__':
    dp.run_polling(bot)
